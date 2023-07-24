# The whole rooms logic, used in views
from django.contrib.auth.hashers import make_password
from users.serializers import RoomSerializer, JoinedRoomSerializer
from .models import Room, User, UserRoom

#---------RoomCreation---------#

def create_room(request) -> dict:
    """Room creation function"""

    # request data
    room_unique_id = request.data.get('room_unique_id')
    room_name = request.data.get('room_name')
    room_owner = request.data.get('room_owner')
    room_password = request.data.get('room_password')
    
    # Check if room owner is existing user in the database (should be existing)
    if User.objects.get(id=room_owner) is None:
        return {'Error': 'Owner of the room does not exist.'}
    
    # Get current user info
    user = User.objects.get(id=room_owner)

    # If room name is not custom set, the default is <ownerUsername>'s room
    if room_name == None or room_name.isspace() or room_name == '':
        room_name = f"{user.username}'s room"

    # Hash room password, if there is one
    room_password = None if room_password is None or room_password == "" else make_password(room_password)

    # create a Room
    room = Room.objects.create(
        room_unique_id=room_unique_id,
        room_name=room_name,
        room_password=room_password,
        owner=user
    )
    
    # Add the room owner to the users of the room, when creating
    room.users.add(user)
    return {'Success': 'Room created'}


def delete_room(request) -> dict:
    """Delete room function"""

    # Get room unique ID
    room_unique_id = request.data.get('room_unique_id')

    # Try deleting room
    try:
        Room.objects.get(room_unique_id=room_unique_id).delete()
        return {"Success": "Room deleted"}
    except Room.DoesNotExist:
        return {"Error": "Room does not exist"}


def edit_room(request) -> dict:
    """Edit room function"""

    # Get unique ID
    room_unique_id = request.data.get('room_unique_id')
    new_room_name = request.data.get('room_name')
    new_room_password = request.data.get('room_password')

    try:
        if Room.objects.filter(room_unique_id=room_unique_id).exists():
            room_to_edit = Room.objects.get(room_unique_id=room_unique_id)
            if new_room_name:
                room_to_edit.room_name = new_room_name
            if new_room_password:
                room_to_edit.room_password = make_password(new_room_password)
            room_to_edit.save()
        return {"Success": "Room edited"}
    except Room.DoesNotExist:
        return {"Error": "Room does not exist"}


def get_room(request) -> dict:
    """Get room function"""

    all_rooms_obj = Room.objects.all()
    serialized = RoomSerializer(all_rooms_obj, many=True)

    try:
        return serialized
    except Room.DoesNotExist:
        return {"Error": serialized.data}

#---------JoinRoom---------#

def join_room(request) -> dict:
    """Join a room"""

    # Get request data
    user_to_join = request.data.get('user')
    room_to_join = request.data.get('room')

    # Check if request user exists
    user = User.objects.get(id=user_to_join)
    if user is None:
        raise User.DoesNotExist

    # Check if request room exists
    room = Room.objects.get(room_unique_id=room_to_join)
    if room is None:
        raise Room.DoesNotExist

    # Get password input from user
    password_input = request.data.get('password')

    # Check if request password == room_password, if there is one
    is_passowrd_matching = False
        
    if room.room_password != None:
        # If both hashed passwords are matching, set is_password_matching to True
        is_passowrd_matching = make_password(password_input) == room.room_password
    else:
        # The room password == None
        is_passowrd_matching = True
    
    # If matching passwords, user can join
    if is_passowrd_matching:
        # if user in Room.objects.filter(room_unique_id=room): #fixit
        #     return {"Error": "The user is already in that room"}
        # else:
        room.users.add(user)
        return {"Success": "User joined the room"}
    else:
        return {"Error": "Room password does not match"}


def leave_room(request) -> dict:
    """User option to leave the room"""

    user_to_leave = request.data.get("user")
    room_to_leave = request.data.get("room")

    room = Room.objects.get(room_unique_id=room_to_leave)
    user = User.objects.get(id=user_to_leave)

    if Room.objects.get(room_unique_id=room.room_unique_id) and User.objects.get(id=user.pk):
        try:
            # Remove the User from the room
            room.users.remove(user)

            # Check if room is empty everytime someone leaves. Delete if so
            if not UserRoom.objects.filter(room_id=room.room_unique_id).exists():
                room.delete()
                # Add a message where it says "Room deleted" in the logger
            return {"Success": "User left the room"}
        except user.DoesNotExist:
            return {"Error": "User is not in the room"}
    else:
        return {"Error": "No such room or user"}


def list_rooms_user_participates(request) -> dict: # needs fix
    """Display all the room, which the current user participates in"""
    user_id = request.data.get("user")

    # Check if it is an existing user in DB
    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
        all_rooms_for_user = UserRoom.objects.filter(user_id=user.pk)
        serialized = JoinedRoomSerializer(all_rooms_for_user, many=True)
        try:
            return serialized
        except Room.DoesNotExist:
            return {"Error": serialized.data}
    else:
        return {"Error": "No such user"}
    

# TODO: Display rooms for currently logged user

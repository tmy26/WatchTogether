# The whole rooms logic, used in views
from django.contrib.auth.hashers import make_password
from users.serializers import RoomSerializer
from .models import Room, User

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
    if room_name == None:
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
    
    if is_passowrd_matching:
        # If matching passwords, user can join
        room.users.add(user)
        return {"Success": "User joined the room"}
    else:
        return {"Error": "Room password does not match"}

# TODO: Display rooms for currently logged user

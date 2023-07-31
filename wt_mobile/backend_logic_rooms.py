# The whole rooms logic, used in views
from django.contrib.auth.hashers import make_password
from .models import Room, User
from wt_mobile.serializers import RoomSerializer
from django.core.exceptions import MultipleObjectsReturned


# ---------Constants--------- #

ERROR = "Error"
SUCCESS = "Success"

#---------RoomCreation---------#

def create_room(request) -> dict:
    """Room creation function"""

    # request data
    unique_id = request.data.get('unique_id')
    name = request.data.get('name')
    owner = request.data.get('owner_id')
    password = request.data.get('password')
    
    # Check if room owner is existing user in the database (should be existing)
    if not User.objects.filter(id=owner).exists():
        return {ERROR: 'Owner of the room does not exist.'}
    
    # Get current user info
    user = User.objects.get(id=owner)

    # If room name is not custom set, the default is <ownerUsername>'s room
    if name == None or name.isspace() or name == '':
        name = f"{user.username}'s room"

    # Hash room password, if there is one
    password = None if password is None else make_password(password)

    # create a Room
    room = Room(
        unique_id=unique_id,
        name=name,
        password=password,
        owner=user
    )

    room.save()

    # Add the room owner to the users of the room, when created
    return {SUCCESS: 'Room created'}


def delete_room(request) -> dict:
    """Delete room function"""

    # Get room unique ID
    unique_id = request.data.get('unique_id')

    # Try deleting room
    try:
        Room.objects.get(unique_id=unique_id).delete()
        return {SUCCESS: "Room deleted"}
    except Room.DoesNotExist:
        return {SUCCESS: "Room does not exist"}


def edit_room(request) -> dict:
    """Edit room function"""

    # Get unique ID
    unique_id = request.data.get('unique_id')
    new_name = request.data.get('new_name')
    new_password = request.data.get('new_password')

    try:
        if Room.objects.filter(unique_id=unique_id).exists():
            room_to_edit = Room.objects.get(unique_id=unique_id)
            if new_name:
                room_to_edit.name = new_name
            if new_password:
                room_to_edit.password = make_password(new_password)
            room_to_edit.save()
        return {SUCCESS: "Room edited"}
    except Room.DoesNotExist:
        return {"Error": "Room does not exist"}


def get_room(request) -> dict:
    """Get room function"""

    all_rooms_obj = Room.objects.all()
    serialized = RoomSerializer(all_rooms_obj, many=True)

    try:
        return serialized
    except Room.DoesNotExist:
        return {SUCCESS: "Room does not exist"}


def join_room(request) -> dict:
    """Join a room"""
    pass
# TODO: Investigate on how to join a room using the GET method.
# TODO: Display rooms for currently logged user

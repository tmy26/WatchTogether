# The whole rooms logic, used in views
from django.contrib.auth.hashers import make_password

from users.serializers import RoomSerializer
from .models import Room, User

def create_room(request) -> dict:
    """Room creation function"""

    # request data
    room_unique_id = request.data.get('room_unique_id')
    room_name = request.data.get('room_name')
    room_owner = request.data.get('room_owner')
    room_password = request.data.get('room_password')

    # Check if room has a unique ID (it should be unique by default)
    if Room.objects.filter(room_unique_id=room_unique_id).exists():
        return {'Error': 'Existing room ID in database'}
    
    # Check if room owner is existing user in the database (should be existing)
    if not Room.objects.filter(room_owner=room_owner).exists():
        return {'Error': 'Owner of the room does not exist.'}
    
    # later will be set default to the logged username's room
    if room_name == None:
        room_name = " "

    # Hash room password, if there is one
    room_password = "" if room_password is None else make_password(room_password)

    # create a Room
    Room.objects.create(
        room_unique_id = room_unique_id,
        room_name=room_name,
        room_password=room_password,
        room_owner=User.objects.get(id=room_owner)
    )
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
        return {"Rooms": serialized.data}
    except Room.DoesNotExist:
        return {"Error": serialized.data}


def join_room(request) -> dict:
    """Join a room"""
    pass
# TODO: Investigate on how to join a room using the GET method.
# TODO: Display rooms for currently logged user

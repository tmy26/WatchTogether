# The whole rooms logic, used in views
from django.contrib.auth.hashers import make_password
from .models import Room
from rest_framework.response import Response


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
    #TODO: Check if room has a owner in database

    # Hash room password
    hash_password = make_password(room_password)

    # create a Room
    Room.objects.create(
        room_unique_id = room_unique_id,
        room_name=room_name,
        room_password=hash_password,
    )
    return {'Success': 'Room created'}

# TODO: GET, POST, DELETE methods for rooms, join a room method
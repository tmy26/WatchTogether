# The whole rooms logic, used in views
from django.contrib.auth.hashers import make_password, check_password
from .models import Room, User, UserRoom
from .serializers import RoomSerializer, JoinedRoomSerializer
from django.core.exceptions import MultipleObjectsReturned
from watch_together.general_utils import get_loggers
from uuid import UUID

# ---------Defines--------- #

# dev_loggers = get_loggers('wt_mobile_dev')
ERROR = 'Error'
SUCCESS = 'Success'

ERROR_MSG = {ERROR: 'Provided data is wrong'}

dev_logger = get_loggers('wt_mobile_dev')


# ---------RoomCreation--------- #

def create_room(request) -> dict:
    """Room creation function"""

    # request data
    unique_id = request.data.get('unique_id')
    name = request.data.get('name')
    owner = request.data.get('owner_id')
    password = request.data.get('password')

    # Check request data validity
    if not is_uuid(unique_id) or not is_int(owner):
        return ERROR_MSG

    # Check if room owner is existing user in the database (should be existing)
    if not User.objects.filter(id=owner).exists():
        return {ERROR: 'Owner of the room does not exist.'}

    # Get current user info
    user = User.objects.get(id=owner)

    # If room name is not custom set, the default is <ownerUsername>'s room
    if name is None or name.isspace() or name == '':
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
    dev_logger.info(msg='A new room was created sucessfully')

    # Add the room owner to the users of the room, when created
    room.users.add(user)
    return {SUCCESS: 'Room created'}


def delete_room(request) -> dict:
    """Delete room function"""

    # Get room unique ID
    unique_id = request.data.get('unique_id')

    # Check request data validity
    if not is_uuid(unique_id):
        return ERROR_MSG

    # Try deleting room
    try:
        Room.objects.get(unique_id=unique_id).delete()
    except (Room.DoesNotExist, MultipleObjectsReturned):
        return ERROR_MSG
    return {SUCCESS: 'Room deleted'}


def edit_room(request) -> dict:
    """Edit room function"""

    # Get unique ID
    unique_id = request.data.get('unique_id')
    new_name = request.data.get('new_name')
    new_password = request.data.get('new_password')

    # Check request data validity
    if not is_uuid(unique_id):
        return ERROR_MSG

    try:
        if Room.objects.filter(unique_id=unique_id).exists():
            room_to_edit = Room.objects.get(unique_id=unique_id)
            if new_name:
                room_to_edit.name = new_name
            if new_password:
                room_to_edit.password = make_password(new_password)
            room_to_edit.save()
    except (Room.DoesNotExist, MultipleObjectsReturned):
        return ERROR_MSG
    return {SUCCESS: 'Room edited'}


def get_room() -> dict:
    """Get room function"""

    try:
        all_rooms_obj = Room.objects.all()
        serialized = RoomSerializer(all_rooms_obj, many=True)
    except Room.DoesNotExist:
        return {ERROR: 'Room does not exist'}
    return serialized


# ---------JoinRoom--------- #

def join_room(request) -> dict:
    """Join a room"""

    # Get request data
    user_to_join = request.data.get('user')
    room_to_join = request.data.get('room')
    # Check if request 'user' is ID and 'room' is UUID
    if not isinstance(user_to_join, int) or not is_uuid(room_to_join):
        return ERROR_MSG
    
    password_input = request.data.get('password')

    # Check if request data exists
    try:
        user = User.objects.get(id=user_to_join)
        room = Room.objects.get(unique_id=room_to_join)
    except (User.DoesNotExist, Room.DoesNotExist, MultipleObjectsReturned):
        return ERROR_MSG

    # Check if the user is already joined to that room
    if UserRoom.objects.filter(room_id=room_to_join, user_id=user_to_join).exists():
        return {ERROR: "User already in the room"}

    # Check if password from request == room password, if there is one
    is_password_matching = False

    if room.password is not None:
        # If both hashed passwords are matching, set is_password_matching to True
        if check_password(password_input, room.password):
            is_password_matching = True
    else:
        # The room password == None
        is_password_matching = True

    # If matching passwords, user can join
    if is_password_matching:
        # TODO: Check if the user already in the party
        room.users.add(user)
    else:
        return {ERROR: 'Provided password did not match the room password'}
    return {SUCCESS: 'User joined the room'}


def leave_room(request) -> dict:
    """User option to leave the room"""

    user_to_leave = request.data.get('user')
    room_to_leave = request.data.get('room')

    # Check request data validity
    if not is_uuid(room_to_leave) or not is_int(user_to_leave):
        return ERROR_MSG

    # Get room and user from db
    try:
        user = User.objects.get(id=user_to_leave)
        room = Room.objects.get(unique_id=room_to_leave)

        # Check if the user is in that room
        if not UserRoom.objects.filter(room_id=room_to_leave, user_id=user_to_leave).exists():
            return {ERROR: "User is not in the room"}

        # Remove the user from the room
        room.users.remove(user)

        # If the room is empty, it will not exist in UserRoom db. Delete the room if so
        if not UserRoom.objects.filter(room_id=room.unique_id).exists():
            room.delete()
            dev_logger.info('Room deleted, because all users left')
    except (User.DoesNotExist, Room.DoesNotExist, MultipleObjectsReturned):
        return ERROR_MSG
    return {SUCCESS: 'User left the room'}


def list_rooms_user_participates(request) -> dict:
    """Display all the rooms, which are user participates in"""

    user_id = request.data.get('user')

    # Check if user ID is an integer
    if not is_int(user_id):
        return ERROR_MSG

    # Return all rooms, that user participates in, if the user exists
    try:
        user = User.objects.get(id=user_id)
        all_rooms_for_user = UserRoom.objects.filter(user_id=user.pk)
        serialized = JoinedRoomSerializer(all_rooms_for_user, many=True)

    except (User.DoesNotExist, Room.DoesNotExist, MultipleObjectsReturned):
        return ERROR_MSG
    return serialized


# ---------Support Functions--------- #

def is_uuid(id):
    """Check if data=uuid"""
    try:
        UUID(str(id))

        return True
    except ValueError:
        return False


def is_int(id):
    """Check if provided data is int, because pk are integers"""

    if isinstance(id, int):
        return True
    else:
        return False
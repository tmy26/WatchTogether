# The whole rooms logic, used in views
import re
import shortuuid
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from watch_together.general_utils import get_loggers
from .utils import UserUtils
from .exceptions import (IllegalArgumentError, PasswordsDoNotMatch,
                         UserAlreadyInRoom, UserIsNotInTheRoom)
from .models import Room, User, UserRoom
from .serializers import JoinedRoomSerializer

# ---------Defines--------- #


SUCCESS = 'Success'
DO_NOT_EXIST = 'Either the user or the room does not exist!'

dev_logger = get_loggers('dev_logger')
client_logger = get_loggers('client_logger')


# ---------RoomCreation--------- #

def create_room(request) -> dict:
    """ Room creation function """

    # request data
    name = request.data.get('name')
    password = request.data.get('password')
    token = request.META.get('HTTP_AUTHORIZATION')

    user = UserUtils.findUser(token)
    owner = user.id

    # Check request data validity
    if not is_int(owner):
        raise IllegalArgumentError('Illegal input.')

    # Check if room owner is existing user in the database (should be existing)
    if not User.objects.filter(id=owner).exists():
        raise ObjectDoesNotExist('User does not exist!')

    # Get current user info
    user = User.objects.get(id=owner)

    # If room name is not custom set, the default is <ownerUsername>'s room
    if name is None or name.isspace() or name == '':
        name = f"{user.username}'s room"
    else:
        # Remove trailing whitespaces and unwanted tabs
        name = re.sub('\s{2,}', ' ', name)

    # Hash room password, if there is one
    password = None if password is None else make_password(password)

    # Get unique ID
    unique_id = get_unique_id()

    # create a Room
    room = Room(
        name=name,
        password=password,
        owner=user,
        unique_id=unique_id
    )

    room.save()
    

    # Add the room owner to the users of the room, when created
    room.users.add(user)

    info = 'A new room was created sucessfully!'
    client_logger.info(msg=info)
    return {SUCCESS: info}


def delete_room(request) -> dict:
    """ Delete room function """

    # Get room unique ID
    unique_id = request.data.get('unique_id')

    # Try deleting room
    try:
        Room.objects.get(unique_id=unique_id).delete()
    except Room.DoesNotExist: 
        raise ObjectDoesNotExist('Room does not exist!')
    except MultipleObjectsReturned:
        dev_logger.error(msg='Multiple objects were returned in delete_room function in backend_logic_rooms, something is wrong with the database!')
        raise MultipleObjectsReturned('Multiple objects returned')
    info = 'Successfully deleted the room!'
    client_logger.info(msg=info)
    return {SUCCESS: info}


def edit_room(request) -> dict:
    """ Edit room function """

    # Get unique ID
    unique_id = request.data.get('unique_id')
    new_name = request.data.get('new_name')
    new_password = request.data.get('new_password')
    # old_password - if the room has one

    # If fields are empty consider them as a null
    if new_name:
        if len(new_name) < 1 or not new_name.isascii():
            new_name = None
        else:
            # Remove trailing whitespaces and unwanted tabs
            new_name = re.sub('\s{2,}', ' ', new_name)

    if new_password:
        if len(new_password) < 1:
            new_password = None

    try:
        Room.objects.filter(unique_id=unique_id).exists()
        room_to_edit = Room.objects.get(unique_id=unique_id)
        if new_name != None:

            if room_to_edit.password != None:
                old_password = request.data.get('old_password')

                if old_password != room_to_edit.password:
                    raise PasswordsDoNotMatch('Old password of room does not match')

            room_to_edit.name = new_name

        if new_password != None:
            if room_to_edit.password != None:
                old_password = request.data.get('old_password')

                if old_password != room_to_edit.password:
                    raise PasswordsDoNotMatch('Old password of room does not match')

            room_to_edit.password = make_password(new_password)
            
        room_to_edit.save()

        return {SUCCESS: 'Room edited'}
    except Room.DoesNotExist:
        raise ObjectDoesNotExist('Room does not exist!')
    except MultipleObjectsReturned:
        dev_logger.error(msg='Multiple objects were returned by edit_room in backend_logic_rooms, there is something wrong with the database!')
        raise MultipleObjectsReturned('Multiple objects returned')
    except PasswordsDoNotMatch as e:
        raise PasswordsDoNotMatch(str(e))


# ---------JoinRoom--------- #

def join_room(request) -> dict:
    """ Join a room """

    # Get request data
    token = request.META.get('HTTP_AUTHORIZATION')
    user_to_join = UserUtils.findUser(token)
    room_to_join = request.data.get('room')

    # Check if request 'user' is ID
    if not isinstance(user_to_join.id, int):
        raise IllegalArgumentError('Illegal input.')
    
    password_input = request.data.get('password')

    # Check if request data exists
    try:
        user = User.objects.get(id=user_to_join.id)
        room = Room.objects.get(unique_id=room_to_join)
    except (User.DoesNotExist, Room.DoesNotExist) as e: 
        # raise with different error msg depending on exception
        if e is User.DoesNotExist():
            raise ObjectDoesNotExist('User does not exist!')
        elif e is Room.DoesNotExist():
            raise ObjectDoesNotExist('Room does not exist!')

    except MultipleObjectsReturned:
        dev_logger.error(msg='Multiple objects were returned in join_room func in backend_logic_rooms, something is wrong with the database!')
        raise MultipleObjectsReturned('Multiple objects returned')

    # Check if the user is already joined to that room
    if UserRoom.objects.filter(room_id=room_to_join, user_id=user_to_join).exists():
        info_err = 'The user is already in the room!'
        client_logger.info(msg=info_err)
        raise UserAlreadyInRoom(info_err)

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
        room.users.add(user)
    else:
        err = 'Provided password did not match the room password'
        client_logger.error(msg=err)
        raise PasswordsDoNotMatch(err)
    info = 'User joined the room'
    client_logger.info(msg=info)
    return {SUCCESS: info}


def leave_room(request) -> dict:
    """ User option to leave the room """

    token = request.META.get('HTTP_AUTHORIZATION')
    user_to_leave = UserUtils.findUser(token)
    room_to_leave = request.data.get('room')

    # Get room and user from db
    try:
        user = User.objects.get(id=user_to_leave.id)
        room = Room.objects.get(unique_id=room_to_leave)

        # Check if the user is in that room
        if not UserRoom.objects.filter(room_id=room_to_leave, user_id=user_to_leave).exists():
            info = 'User is not in the room'
            client_logger.info(msg=info)
            raise UserIsNotInTheRoom(info)

        # Remove the user from the room
        room.users.remove(user)

        # If the room is empty, it will not exist in UserRoom db. Delete the room if so
        if not UserRoom.objects.filter(room_id=room.unique_id).exists():
            room.delete()
        # Check if the user who leaves is the owner of the room, reassign the owner if the room is not empty
        elif user == room.owner:
            # Get the first joined user, after the creator
            id_of_next_owner = UserRoom.objects.filter(room_id=room_to_leave).first()

            # Reassign room owner to the first joined user, if the current owner gets deleted
            reassign_owner(room, id_of_next_owner)

    except (User.DoesNotExist, Room.DoesNotExist) as e:
        client_logger.error(msg=DO_NOT_EXIST)
        # raise with different error msg depending on exception
        if e is User.DoesNotExist():
            raise ObjectDoesNotExist('User does not exist!')
        elif e is Room.DoesNotExist():
            raise ObjectDoesNotExist('Room does not exist!')

    except MultipleObjectsReturned:
        dev_logger.error(msg='Multiple objects returned at leave_room in backend_logic_rooms, there is something wrong with the db!')
        raise MultipleObjectsReturned('Multiple objects returned.')
    return {SUCCESS: 'User left the room'}


def list_rooms_user_participates(request) -> dict:
    """ Display all the rooms, which are user participates in """

    user_id = get_owner_id_from_token(request)

    # Check if user ID is an integer
    if not is_int(user_id):
        raise IllegalArgumentError('Illegal input.')

    # Return all rooms, that user participates in, if the user exists
    try:
        user = User.objects.get(id=user_id)
        all_rooms_for_user = UserRoom.objects.filter(user_id=user.pk)
        serialized = JoinedRoomSerializer(all_rooms_for_user, many=True)

    except (User.DoesNotExist, Room.DoesNotExist) as e: 
        client_logger.error(msg=DO_NOT_EXIST)

        # raise with different error msg depending on exception
        if e is User.DoesNotExist():
            raise ObjectDoesNotExist('User does not exist!')
        elif e is Room.DoesNotExist():
            raise ObjectDoesNotExist('Room does not exist!')

    except MultipleObjectsReturned:
        dev_logger.error(msg='Multiple objects returned in list_rooms_user_participates in backend_logic_rooms, there is something wrong with the db!')
        raise MultipleObjectsReturned('Multiple objects returned.')
    return serialized


# ---------Support Functions--------- #

def is_int(id):
    """ Check if provided data is int, because pk are integers """

    if isinstance(id, int):
        return True
    else:
        return False


def reassign_owner(room, id_next_owner):
    """ Reassign room owner to the first joined user, if the current owner gets deleted """

    try:
        # Get the instance of the next onwer
        new_owner = User.objects.get(id=id_next_owner.user_id)

        # Change owner to the first joined user
        room.owner = new_owner
        room.save()
    except (Room.DoesNotExist, User.DoesNotExist):
        client_logger.info(msg=DO_NOT_EXIST)
        raise ObjectDoesNotExist('Could not reassign the owner of the room')
    except MultipleObjectsReturned:
        dev_logger.error(msg='Multiple objects returned in reassing_owner in backend_logic_room, there is something wrong with the database!')
        raise MultipleObjectsReturned('Could not reassign the owner of the room')
    return {SUCCESS: 'The owner of the room was changed'}


def get_unique_id():
    """ Generates unique ID for room """
    
    while True:
        unique_id = shortuuid.ShortUUID().random(length=6)

        if Room.objects.filter(unique_id=unique_id).count() == 0:
            break
    return unique_id


def get_owner_id_from_token(request):
    """ Gets the owner id from token """

    token = request.META.get('HTTP_AUTHORIZATION')
    user = UserUtils.findUser(token)

    if user is None:
        raise ObjectDoesNotExist('User not found!')

    return user.id

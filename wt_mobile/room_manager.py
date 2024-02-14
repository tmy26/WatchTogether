import re
import shortuuid
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import JsonResponse
from watch_together.general_utils import get_loggers
from .exceptions import (IllegalArgumentError, PasswordsDoNotMatch,
                         UserAlreadyInRoom, UserIsNotInTheRoom, RoomNameNotProvided, UserPasswordIsTooShort)
from .models import Room, User, UserRoom
from .serializers import JoinedRoomSerializer
from .utils import UserUtils

dev_logger = get_loggers('dev_logger')


class RoomManager(object):
    """This class contains the following operations for Room:
    1. Support methods
    2. Create room
    3. Delete room
    4. Edit room
    5. Join room
    6. Leave room
    7. List all rooms that user participates in
    """
    def _is_int(self, id: int) -> bool:
        """
        Checks if provided parameter is int.
        :param id: the parameter that is going to be checked
        :type id: int
        :rType: boolean
        :returns: Boolean, if the provided parameter (id) is int returns True, else False.
        """
        if isinstance(id, int):
            return True
        else:
            return False

    def _reassign_owner(self, room: object, id_next_owner: int) -> dict:
        """
        Reassign the room owner to the first user who joined, in case the current owner is deleted.
        :param room: the room as object
        :type room: object
        :param id_next_owner: the ID of the upcoming user who will become the owner of the room.
        :type id_next_owner: int
        :rType: dictionary
        :returns: A message indicating the successful completion of the function.
        """
        try:
            # Get the instance of the next onwer
            new_owner = User.objects.get(id=id_next_owner.user_id)

            # Change owner to the first joined user
            room.owner = new_owner
            room.save()
            return {'Success': 'The owner of the room was changed'}
        except (Room.DoesNotExist, User.DoesNotExist):
            raise ObjectDoesNotExist('Could not reassign the owner of the room!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the reassign_owner process in room_manager.py'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)

    def _get_unique_id(self) -> int:
        """
        Generates unique ID for room.
        :rType: int
        :returns: Room's unique id.
        """
        while True:
            unique_id = shortuuid.ShortUUID().random(length=6)

            if Room.objects.filter(unique_id=unique_id).count() == 0:
                break
        return unique_id

    def _edit_room_password(request, unique_id: int):
        """
        Edit room password used in edit_room functionality
        """
        new_password = request.data.get('new password')
        
        try:
            if new_password is not None:
                new_password = new_password.strip()
            else:
                raise IllegalArgumentError("Illegal input for password")
            if new_password:
                if len(new_password) < 5:
                    raise UserPasswordIsTooShort("New password is too short. It must be at least 5 characters long.")
            
                if new_password != None:
                    Room.objects.filter(unique_id=unique_id).exists()
                    room_to_edit = Room.objects.get(unique_id=unique_id)
                    room_to_edit.password = make_password(new_password)
                    room_to_edit.save()
                    return {'Success': 'The password of the room was successfuly changed!'}
            else:
                raise UserPasswordIsTooShort("New password is too short. It must be at least 5 characters long.")
        except Room.DoesNotExist:
            raise ObjectDoesNotExist('Room does not exist!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the edit_room process in room_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)

    def _edit_room_name(request, unique_id: int) -> dict:
        """
        Edit room's name. Used in edit_room functionality
        """
        new_name = request.data.get('new name')

        try:
            if new_name:
                if len(new_name) < 1 or not new_name.isascii():
                    new_name = None
                else:
                    new_name = re.sub("\'s{2,}", ' ', new_name)

            Room.objects.filter(unique_id=unique_id).exists()
            room_to_edit = Room.objects.get(unique_id=unique_id)
            if new_name != None:
                room_to_edit.name = new_name
                room_to_edit.save()
                return {'Success': 'The name of the room was successfully changed!'}
            else:
                raise RoomNameNotProvided('Invalid room name, please try again with another!')
        except Room.DoesNotExist:
            raise ObjectDoesNotExist('Room does not exist!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the edit_room process in room_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)
       

    @classmethod
    def create_room(cls, request) -> dict:
        """
        Create new room.
        :param name: room name
        :type name: string
        :param password: room's password
        :type password: string
        :param token: the user token serves the purpose of identifying the user
        :type token: string
        :rType: dictionary
        :returns: A message indicating the successful completion of the function.
        """
        name = request.data.get('name')
        password = request.data.get('password')
        token = request.META.get('HTTP_AUTHORIZATION')

        user = UserUtils.findUser(token)
        owner = user.id

        if not cls._is_int(self=cls, id=owner):
            raise IllegalArgumentError('Illegal input!')

        if not User.objects.filter(id=owner).exists():
            raise ObjectDoesNotExist('Sorry, we could not find the user you are looking for!')

        user = User.objects.get(id=owner)
        if name is None or name.isspace() or name == '':
            name = f"{user.username}'s room"
        else:
            name = re.sub("\'s{2,}", ' ', name)

        # password validator
        if password is not None:
            password = password.strip()

        # python consideres empty strings as false
        if not password:
            password = None
        elif len(password) < 5:
            raise UserPasswordIsTooShort("Password is too short. Must have at least 5 characters")

        password = None if password is None else make_password(password)


        unique_id = cls._get_unique_id(self=cls)
        room = Room(
            name=name,
            password=password,
            owner=user,
            unique_id=unique_id
        )
        room.save()
        room.users.add(user)
        return {'Success': 'A new room was created sucessfully!'}

    @staticmethod
    def delete_room(request) -> dict:
        """
        Delete room.
        :param unique_id: room's unique id
        :type unique_id: string
        :rType dictionary:
        :returns: A message indicating the successful completion of the function.
        """
        unique_id = request.data.get('unique_id')

        # Try deleting room
        try:
            Room.objects.get(unique_id=unique_id).delete()
        except Room.DoesNotExist: 
            raise ObjectDoesNotExist('Room does not exist!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the delete_room function in room_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)
        return {'Success': 'Room deleted!'}

    @classmethod
    def edit_room(cls, request) -> dict:
        """
        Edit room properties
        :param unique_id: room's unique identifier
        :type unique_id: int
        :param field to edit: choose which field of room will be edited
        :rType: dict
        :returns: a message which indicates success
        :exceptions: UserPasswordIsTooShort, ObjectDoesNotExist, Room.DoesNotExist, MultipleObjectsReturned
        """

        unique_id = request.data.get('unique_id')
        field_to_edit = request.data.get('field to edit')

        match field_to_edit:
            case "name":
                # requests new name -> "new name"
                return cls._edit_room_name(request, unique_id)

            case "password":
                # requests new password -> "new password"
                return cls._edit_room_password(request, unique_id)

    @staticmethod
    def join_room(request) -> dict:
        """
        Add user into a room.
        :param token: the user token serves the purpose of identifying the user
        :type token: string
        :param room_to_join: the room that the user is going to join
        :type room_to_join: string
        :rType: dictionary
        :returns: A message indicating the successful completion of the function.
        """
        token = request.META.get('HTTP_AUTHORIZATION')
        room_to_join = request.data.get('room')
        user_to_join = UserUtils.findUser(token)
        password_input = request.data.get('password')

        if not isinstance(user_to_join.id, int):
            raise IllegalArgumentError('Illegal input.')

        try:
            user = User.objects.get(id=user_to_join.id)
            room = Room.objects.get(unique_id=room_to_join)
        except (Room.DoesNotExist): 
            raise ObjectDoesNotExist('Room does not exist!')
        except (User.DoesNotExist):
            raise ObjectDoesNotExist('User does not exist!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the join_room function in room_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)

        if UserRoom.objects.filter(room_id=room_to_join, user_id=user_to_join).exists():
            info_err = 'The user is already in the room!'
            raise UserAlreadyInRoom(info_err)

        is_password_matching = False

        if password_input is not None:
            password_input = password_input.strip()

        if room.password is not None:
            if check_password(password_input, room.password):
                is_password_matching = True
        else:
            is_password_matching = True

        if is_password_matching:
            room.users.add(user)
        else:
            err = 'Provided password did not match the room password'
            raise PasswordsDoNotMatch(err)
        return {'Success': 'User joined the room'}

    @classmethod
    def leave_room(cls, request) -> dict:
        """
        Remove a user from room.
        :param token: the user token serves the purpose of identifying the user
        :type token: string
        :param room_to_leave: the ID of the room the user intends to leave
        :type room_to_leave: string
        :rType: dictionary
        :returns: A message indicating the successful completion of the function.
        """
        token = request.META.get('HTTP_AUTHORIZATION')
        room_to_leave = request.data.get('room')
        user_to_leave = UserUtils.findUser(token)

        # Get room and user from db
        try:
            user = User.objects.get(id=user_to_leave.id)
            room = Room.objects.get(unique_id=room_to_leave)

            if not UserRoom.objects.filter(room_id=room_to_leave, user_id=user_to_leave).exists():
                info = 'User is not in the room'
                raise UserIsNotInTheRoom(info)

            room.users.remove(user)
            if not UserRoom.objects.filter(room_id=room.unique_id).exists():
                room.delete()
            elif user == room.owner:
                id_of_next_owner = UserRoom.objects.filter(room_id=room_to_leave).first()
                cls._reassign_owner(self=cls, room=room, id_next_owner=id_of_next_owner)
            return {'Success': 'User left the room'}
        except (User.DoesNotExist, Room.DoesNotExist) as error:
            if error is User.DoesNotExist():
                raise ObjectDoesNotExist('User does not exist!')
            elif error is Room.DoesNotExist():
                raise ObjectDoesNotExist('Room does not exist!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the leave_room process in room_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)

    @classmethod
    def get_user_participating_rooms(cls, request) -> JsonResponse:
        """
        Show all rooms in which the user is participating.
        :param token: the user token serves the purpose of identifying the user
        :type token: string
        :rType: JSON Response
        :returns: Serialized object, with all rooms that the user participate.
        """
        token = request.META.get('HTTP_AUTHORIZATION')
        user = UserUtils.findUser(token)

        if user is None:
            raise ObjectDoesNotExist('User not found!')
        user_id = user.id

        if not cls._is_int(self=cls, id=user_id):
            raise IllegalArgumentError('Illegal input.')

        # Return all rooms, that user participates in, if the user exists
        try:
            user = User.objects.get(id=user_id)
            all_user_rooms = UserRoom.objects.filter(user_id=user.pk)

            all_rooms_for_user = []

            for room in all_user_rooms:
                all_rooms_for_user.append(Room.objects.get(unique_id=room.room_id))

            serialized = JoinedRoomSerializer(all_rooms_for_user, many=True)
            return serialized
        except (User.DoesNotExist, Room.DoesNotExist) as error: 
            if error is User.DoesNotExist():
                raise ObjectDoesNotExist('User does not exist!')
            elif error is Room.DoesNotExist():
                raise ObjectDoesNotExist('Room does not exist!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the list_rooms_user_participates process in room_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)

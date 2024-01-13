from datetime import datetime
import requests
from django.http import JsonResponse
from django.core.exceptions import (MultipleObjectsReturned, ObjectDoesNotExist, ValidationError)
from watch_together.general_utils import get_loggers
from .exceptions import (StreamAlreadyAssigned, StreamInvalidLink,
                        RoomNotProvided, LinkNotProvided)
from .models import Room, Stream, StreamHistory
from .serializers import StreamHistorySerializer

dev_logger = get_loggers('dev_logger')


class StreamManager(object):
    """This class contains the following operations for Stream:
    1. Create stream
    2. Edit stream
    3. Display history
    4. Validate link
    5. Add to history
    """
    def _validate_link(self, link) -> bool:
        """
        Checks if link is valid.
        :param link: the link which is going to be checked
        :type link: string
        :rType: boolean
        :returns: True if it successfully opens the link, False if there is an issue.
        """
        try:
            response = requests.get(link)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False
    
    def _add_to_history(self, stream):
        """
        Creates a record that shows what was played.
        :param stream: the stream that we are creating the record for.
        :type stream: string
        :rType: dictionary
        :returns: Success message that indicates the operation completed.
        """
        try:
            today = datetime.now()
            time_when_played = today.strftime("%d/%m/%Y %H:%M:%S")

            # if the current link of the stream is valid, add it to the history
            stream_history = StreamHistory(
                stream_id=stream.id,
                time_when_played=time_when_played,
                link=stream.link
            )
            stream_history.save()
            return {'Success': 'Stream link added to history'}
        except (Room.DoesNotExist, Stream.DoesNotExist) as error:
            if error is Room.DoesNotExist():
                raise ObjectDoesNotExist('Room does not exist!')
            else:
                raise ObjectDoesNotExist('Stream does not exist!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the _add_to_history process in stream_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)

    @staticmethod
    def create_stream(request) -> dict:
        """
        Stream creation function.
        :param assigned_room: the room to which the stream is assigned to
        :type assigned_room: string
        :rType: dictionary
        :returns: Success message that indicates the operation completed.
        """
        assigned_room = request.data.get('assigned room')

        try:
            if not assigned_room:
                raise RoomNotProvided('There is no room provided')

            room = Room.objects.get(unique_id=assigned_room)

            # Check if the room already has a stream assigned
            if Stream.objects.filter(assigned_room=room).exists():
                raise StreamAlreadyAssigned('There is an already assigned stream for that room')
            
            # Create and save a new Stream instance
            created_stream = Stream(assigned_room=room)
            created_stream.save()
            return {'Success': 'Stream created'}
        except (ValidationError, requests.exceptions.InvalidURL):
            raise StreamInvalidLink('The provided link is invalid')
        except (MultipleObjectsReturned, Stream.DoesNotExist) as error:
            if error is MultipleObjectsReturned():
                error_msg = 'An issue with the database: Multiple objects were returned during the create_stream process in stream_manager.py!'
                dev_logger.error(msg=error_msg, exc_info=True)
                raise MultipleObjectsReturned(error_msg)
            else:
                raise ObjectDoesNotExist('The given ID does not match any existing room!')
        
    @classmethod
    def edit_stream(cls, request) -> dict:
        """
        Edit stream function.
        :param link: the link that we are going to use to extract the video from
        :type link: string
        :param assigned_room: the room to which the stream is assigned to
        :type assigned_room: string
        :rType: dictionary
        :returns: Success message that indicates the operation completed.
        """
        link = request.data.get('link')
        assigned_room = request.data.get('assigned room')

        try:
            if not link:
                raise LinkNotProvided('A link was not provided!')
            if not assigned_room:
                raise RoomNotProvided('A room was not provided!')
            stream_to_edit = Stream.objects.get(assigned_room=assigned_room)

            # Validate the provided link using the validate_link function
            link_validation_result = cls._validate_link(link)
            if link_validation_result:
                return link_validation_result
                
            # Update the stream link and save the changes
            stream_to_edit.link = link
            stream_to_edit.save()
            cls._add_to_history(stream_to_edit)
            return {'Success': 'The stream link was successfully edited!'}
        except (ValidationError, requests.exceptions.InvalidURL):
            raise StreamInvalidLink('Provided link is not valid.')
        except (MultipleObjectsReturned, Stream.DoesNotExist) as error:
            if error is MultipleObjectsReturned():
                error_msg = 'An issue with the database: Multiple objects were returned during the edit_stream process in stream_manager.py!'
                dev_logger.error(msg=error_msg, exc_info=True)
                raise MultipleObjectsReturned(error_msg)
            else:
                raise ObjectDoesNotExist('The given ID does not match any existing room.')

    @staticmethod
    def display_history(request) -> JsonResponse:
        """
        Display the history of the current stream.
        :param stream_request: the id of the stream
        :type stream_request: string
        :rType: JSON serialized object
        :returns: JSON serialized object.
        """
        stream_request = request.data.get('stream')

        try:
            stream = Stream.objects.get(id=stream_request)
            all_links = StreamHistory.objects.filter(stream_id=stream.pk)
            serialized = StreamHistorySerializer(all_links, many=True)
            return serialized
        except (Stream.DoesNotExist, ValueError):
            raise ObjectDoesNotExist('Stream does not exist!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the display_history process in stream_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)

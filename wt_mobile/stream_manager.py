from datetime import datetime
import requests
from django.core.exceptions import (MultipleObjectsReturned,
                                    ObjectDoesNotExist, ValidationError)
from watch_together.general_utils import get_loggers
from .exceptions import (CommonException, StreamAlreadyAssigned,
                         StreamAssignedRoomRequired, StreamInvalidLink)
from .models import Room, Stream, StreamHistory
from .serializers import StreamHistorySerializer


ERROR = 'Error'
SUCCESS = 'Success'
ERROR_MESSAGE = {'Error': 'Something went wrong with the data you provided. Please check if the data is correct and try again.'}
ERROR_LINK_NOT_VALID = 'The provided link is invalid'

dev_logger = get_loggers('dev_logger')
client_logger = get_loggers('client_logger')


class StreamManager(object):
    """This class contains the following operations for Stream:
    1. Create stream
    2. Edit stream
    3. Display history
    4. Validate link
    5. Add to history
    """
    @staticmethod
    def create_stream(request):
        """
        Stream creation function.
        :param assigned_room: the room to which the stream is assigned to
        :type assigned_room: string
        :rType: dictionary
        :returns: Success message that indicates the operation completed.
        """
        assigned_room = request.data.get('assigned_room')

        try:
            # Check if assigned_room is provided
            if not assigned_room:
                raise StreamAssignedRoomRequired('There is no room provided')

            # Check if the room exists
            room = Room.objects.get(unique_id=assigned_room)

            # Check if the room already has a stream assigned
            if Stream.objects.filter(assigned_room=room).exists():
                raise StreamAlreadyAssigned('There is an already assigned stream for that room')
            
            # Create and save a new Stream instance
            created_stream = Stream(assigned_room=room)
            created_stream.save()
        except (ValidationError, requests.exceptions.InvalidURL):
            client_logger.error(msg=ERROR_LINK_NOT_VALID)
            raise StreamInvalidLink('The provided link is invalid')
        except (MultipleObjectsReturned, Stream.DoesNotExist) as err:
            dev_logger.error(msg=err, exc_info=True)
            if err is MultipleObjectsReturned():
                raise MultipleObjectsReturned(ERROR_MESSAGE)
            else:
                raise ObjectDoesNotExist(ERROR_MESSAGE)

        # Return a success message
        info = 'Stream created'
        client_logger.info(msg=info)
        return {SUCCESS: info}
        
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
        assigned_room = request.data.get('assigned_room')

        # Check if requested data is null
        if not link or not assigned_room:
            raise CommonException('No data provided')
        try:
            # Retrieve the stream to edit
            stream_to_edit = Stream.objects.get(assigned_room=assigned_room)

            # Validate the provided link using the validate_link function
            link_validation_result = cls._validate_link(link)
            if link_validation_result:
                return link_validation_result
                
            # Update the stream link and save the changes
            stream_to_edit.link = link
            stream_to_edit.save()

            cls._add_to_history(stream_to_edit)

        except (ValidationError, requests.exceptions.InvalidURL):
            raise StreamInvalidLink('Provided link is not valid.')
        except (MultipleObjectsReturned, Stream.DoesNotExist) as err:
            dev_logger.error(msg=err, exc_info=True)
            if err is MultipleObjectsReturned():
                raise MultipleObjectsReturned(ERROR_MESSAGE)
            else:
                raise ObjectDoesNotExist(ERROR_MESSAGE)
        info = 'The stream link was successfully edited!'
        client_logger.info(msg=info)
        return {SUCCESS: info}

    @staticmethod
    def display_history(request):
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
        except (Stream.DoesNotExist, ValueError):
            raise ObjectDoesNotExist('Stream does not exist!')
        except MultipleObjectsReturned:
            dev_logger.error('Multiple objects returned in display_history() in backend_logic_stream')
            raise MultipleObjectsReturned('Multiple objects returned!')
        return serialized

    def _validate_link(self, link) -> bool:
        """
        Checks if link is valid.
        :param link: the link which is going to be checked
        :type link: string
        :rType: boolean
        :returns: True if it can open the link, False if something is wrong.
        """
        try:
            response = requests.get(link)
            if response.status_code == 200:
                #if the method is able to open the website it returns none
                return True
            else:
                dev_logger.error(msg='Error: Link is valid, but the website returned a non-OK status code')
                return False
            
        except requests.exceptions.RequestException:
            dev_logger.error(msg='Link is not valid or could not be accessed.')
            return False
        
    def _add_to_history(self, stream):
        """
        Creates a record that shows what was played.
        :param stream: the stream that we are creating the record for.
        :type stream: string
        :rType: dictionary
        :returns: Success message that indicates the operation completed.
        """
        today = datetime.now()
        try:
            time_when_played = today.strftime("%d/%m/%Y %H:%M:%S")

            # if the current link of the stream is valid, add it to the history
            stream_history = StreamHistory(
                stream_id=stream.id,
                time_when_played=time_when_played,
                link=stream.link
            )
            stream_history.save()
            info = 'Stream link added to history'
            client_logger.info(msg=info)
            return {SUCCESS: info}
        except (Room.DoesNotExist, Stream.DoesNotExist) as e:
            if e is Room.DoesNotExist():
                raise ObjectDoesNotExist('Room does not exist!')
            else:
                raise ObjectDoesNotExist('Stream does not exist!')
        except MultipleObjectsReturned:
            dev_logger.error('Multiple objects have returned by add_to_history() in backed_logic_stream')
            raise MultipleObjectsReturned(ERROR_MESSAGE)

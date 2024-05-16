# chat_app/stream_manager.py
from .models import StreamHistory
from wt_mobile.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from watch_together.general_utils import get_loggers
from .serializers import StreamHistorySerializer


dev_logger = get_loggers('dev_logger')


class StreamManager(object):
    """ Chat functionality """

    @staticmethod
    def get_stream_history(request): #TODO: needs fix
        """
        Status codes - 200, 404, 500
        Accepts parameter 'room_id'
        Returns a list of stream history links for a room
        """

        # Fetch messages from the database
        room_id = request.GET.get('room_id')

        # filter the links
        try:
            links = StreamHistory.objects.get(room_id=room_id)
            serialized = StreamHistorySerializer(links, many=True)
            return serialized
        except StreamHistory.DoesNotExist:
            raise ObjectDoesNotExist('Stream for this room do not exist!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the get_stream_history process in stream_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)


# chat_app/chat_manager.py
from .models import Message
from wt_mobile.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from watch_together.general_utils import get_loggers


dev_logger = get_loggers('dev_logger')


class ChatManager(object):
    """ Chat functionality """

    @staticmethod
    def get_previous_messages(request):
        """
        Status codes - 200, 404, 500
        Accepts parameter 'room_id'
        Returns a list of previous chat messages for a room
        """

        # Fetch messages from the database
        room_id = request.GET.get('room_id')

        # filter the messages and return them ordered by time
        try:
            messages = Message.objects.filter(room_id=room_id).order_by('timestamp')
        except Message.DoesNotExist:
            raise ObjectDoesNotExist('Messages for this room do not exist!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the get_previous_messages process in chat_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)

        # Convert messages to JSON format
        message_list = []
        if messages:
            for message in messages:
                try:
                    user = User.objects.get(pk=message.sender_id).username
                except User.DoesNotExist:
                    user = "deleted user"
                except MultipleObjectsReturned:
                    error_msg = 'An issue with the database: Multiple objects were returned during the get_previous_messages process in chat_manager.py!'
                    dev_logger.error(msg=error_msg, exc_info=True)
                    raise MultipleObjectsReturned(error_msg)

                message_dict = {
                    'username': user,
                    'message': message.content,
                }
                message_list.append(message_dict)

        # Return messages
        return message_list

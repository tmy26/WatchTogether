# chat_app/utils.py
from wt_mobile.models import Room
from knox import crypto
from knox.models import AuthToken
from watch_together.general_utils import get_loggers

DEV_LOGGER = get_loggers('dev_logger')

def get_user(token_key):
    """ Verify that header token is valid and get user object """

    user = None
    try:
        token_obj = AuthToken.objects.filter(digest=crypto.hash_token(token_key)).first()
        user = token_obj.user  
    except Exception:
        error_msg = "Getting the User object raised an exception while trying to handshake with WebSocket.\
            Refer to 'get_user()' inside chat_app/utils.py"
        DEV_LOGGER.error(error_msg, exc_info=True)
        return user
    return user

def get_room(unique_id):
    """ Get Room object """

    try:
        room = Room.objects.get(unique_id=unique_id)
        if room is not None:
            return room
    except Exception:
        error_msg = "Getting the Room object raised an exception while trying to handshake with WebSocket.\
            Refer to 'get_room()' inside chat_app/utils.py"
        DEV_LOGGER.error(error_msg, exc_info=True)
        raise Exception

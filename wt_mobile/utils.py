from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from email_validator import EmailNotValidError
from knox import crypto
from knox.models import AuthToken
from watch_together.general_utils import get_loggers
from .exceptions import *
from .tokens import account_activation_token

dev_logger = get_loggers('dev_logger')


class UserUtils(object):
    """This class contains methods for:
    1. Find user's account by token
    2. Send email
    3. User custom exception handlers
    4. Room custom exception handlers
    5. Stream custom exception handlers
    6. Handle response from functions
    """
    @staticmethod
    def findUser(token:str) -> object:
        """
        Searches the db for user that is matching the provided token and returns it
        :param token: the provided token
        :type token: string
        :rType: object
        :returns: Object, either None is User object.
        """
        user = None
        try:
            raw_token = token.split(' ')[1]
            token_obj = AuthToken.objects.filter(digest=crypto.hash_token(raw_token)).first()
            user = token_obj.user
        except Exception:
            return user
        return user
    
    @staticmethod
    def send_email(request, mail_subject: str, template_path: str, user: object, receiver: str) -> None:
            """
            Sends an email containing a verification link necessary for account activation.
            :param mail_subject: what is the email about
            :type mail_object: string
            :param template_path: which template to use from templates folder
            :type template_path: string
            :param user: user object
            :type user: object
            :param receiver: the email adress which will receive the message
            :type receiver: string
            :rType: None
            :returns: None, just logs the state of the message.
            """
            mail_subject = mail_subject
            message = render_to_string(template_path,
            {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
                'new_email': receiver
            })

            email = EmailMessage(subject=mail_subject, body=message, to=[receiver])
            send_email = email.send()
            if send_email:
                return True
            else:
                dev_logger.error(msg='Error. An error occured while trying to send email. Traceback file: function: send_email in file: backend_utils, line 36, in app: wt_mobile', exc_info=True)
                return False

class CustomExceptionUtils(object):
    """This class holds methods for custom exceptions which are related to:
    1. User
    2. Room
    3. Stream
    4. Chat
    """
    @staticmethod
    def user_custom_exception_handler(exception_message) -> JsonResponse:
        """
        Handles custom exceptions raised from user functions.
        :param exception_message: the custom exception that is passed
        :type exception_message: string
        :rType: JsonResponse
        :returns: the proper status code and error message
        """
        match exception_message:
            case EmailAlreadyUsed():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case UsernameAlreadyUsed():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case EmailWasNotProvided():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case UsernameTooShort():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case UserPasswordIsTooShort():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case PasswordsDoNotMatch():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case EmailNotValidError():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case ObjectDoesNotExist():
                response = JsonResponse({'Error': str(exception_message)}, status=404)
            case MultipleObjectsReturned():
                response = JsonResponse({'Error': str(exception_message)}, status=500)
            case UserEmailNotActivated():
                response = JsonResponse({'Error': str(exception_message)}, status=403)
            case MaxNumberAuth():
                response = JsonResponse({'Error': str(exception_message)}, status=431)
            case FieldNotEditable():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case UserAlreadyActivated():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case UsernameNotProvided():
                response = JsonResponse({'Error': str(exception_message)}, status=401)
            case PasswordNotProvided():
                response = JsonResponse({'Error': str(exception_message)}, status=401)
            case _:
                response = JsonResponse({'Error': 'Internal Server Error'}, status=500)
        return response

    @staticmethod
    def room_custom_exception_handler(exception_message):
        """
        Handles custom exceptions raised from room functions.
        :param exception_message: the custom exception that is passed
        :type exception_message: string
        :rType: JsonResponse
        :returns: the proper status code and error message
        """
        match exception_message:
            case IllegalArgumentError():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case ObjectDoesNotExist():
                response = JsonResponse({'Error': str(exception_message)}, status=404)
            case MultipleObjectsReturned():
                response = JsonResponse({'Error': str(exception_message)}, status=500)
            case UserAlreadyInRoom():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case PasswordsDoNotMatch():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case UserIsNotInTheRoom():
                response = JsonResponse({'Error'}, status=400)
            case RoomNameNotProvided():
                response = JsonResponse({'Error': str(exception_message)}, status=406)
            case UserPasswordIsTooShort():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case _:
                response = JsonResponse({'Error': 'Internal Server Error'}, status=500)
        return response

    @staticmethod
    def stream_custom_exception_handler(exception_message):
        """
        Handles custom exceptions raised from stream functions.
        :param exception_message: the custom exception that is passed
        :type exception_message: string
        :rType: JsonResponse
        :returns: the proper status code and error message
        """
        match exception_message:
            case StreamAssignedRoomRequired():
                response = JsonResponse({'Error': str(exception_message)}, status=424)
            case StreamAlreadyAssigned():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case StreamInvalidLink():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case MultipleObjectsReturned():
                response = JsonResponse({'Error': str(exception_message)}, status=500)
            case ObjectDoesNotExist():
                response = JsonResponse({'Error': str(exception_message)}, status=404)
            case LinkNotProvided():
                response = JsonResponse({'Error': str(exception_message)}, status=406)
            case RoomNotProvided():
                response = JsonResponse({'Error': str(exception_message)}, status=406)
            case CommonException():
                response = JsonResponse({'Error': str(exception_message)}, status=400)
            case _:
                response = JsonResponse({'Error': 'Internal Server Error'}, status=500)
        return response
    
    @staticmethod
    def chat_custom_exception_handler(exception_message):
        """
        Handles custom exceptions raised from chat functions.
        :param exception_message: the custom exception that is passed
        :type exception_message: string
        :rType: JsonResponse
        :returns: the proper status code and error message
        """

        match exception_message:
            case MultipleObjectsReturned():
                response = JsonResponse({'Error': str(exception_message)}, status=500)
            case ObjectDoesNotExist():
                response = JsonResponse({'Error': str(exception_message)}, status=404)
            case _:
                response = JsonResponse({'Error': 'Internal Server Error'}, status=500)
        return response


class HandleResponseUtils(object):
    """This class holds methods related to views.py:
    1. The methods here are related to response handling
    """
    @staticmethod
    def handle_response(status_code, message) -> JsonResponse:
        """
        Returns proper response data
        :param status_code: http status code
        :type status_code: http status code
        :param message: function that contains response
        :rType: JsonResponse
        :returns: JsonResponse
        """
        # If the obj is type set return list(obj)
        if isinstance(message, set):
            return JsonResponse(data=list(message), status=status_code, safe=False)
        else:
            return JsonResponse(data=message, status=status_code, safe=False)

    @staticmethod
    def handle_response_data(status_code, message):
        """
        Returns proper response data
        :param status_code: http status code
        :type status_code: http status code
        :param message: function that contains response
        :rType: JsonResponse
        :returns: JsonResponse
        """
        if isinstance(message, set):
            return JsonResponse(data=list(message).data, status=status_code, safe=False)
        else:
            return JsonResponse(data=message.data, status=status_code, safe=False)

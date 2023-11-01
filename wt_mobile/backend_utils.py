from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import JsonResponse
from email_validator import EmailNotValidError
from knox import crypto
from knox.models import AuthToken
from .exceptions import *


def findUser(token:str) -> object:
    user = None
    try:
        raw_token = token.split(' ')[1]
        token_obj = AuthToken.objects.filter(digest=crypto.hash_token(raw_token)).first()
        user = token_obj.user
    except Exception:
        return user
    return user


def user_custom_exception_handler(exc):
    """ Handles custom exceptions raise from user funcs, returning the proper status code and error message """

    match exc:
        case EmailAlreadyUsed():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case UsernameAlreadyUsed():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case EmailWasNotProvided():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case UsernameTooShort():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case UserPasswordIsTooShort():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case PasswordsDoNotMatch():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case EmailNotValidError():
            error = 'The provided email is in a bad format.'
            response = JsonResponse({'Error': error}, status=400)
        case ObjectDoesNotExist():
            response = JsonResponse({'Error': str(exc)}, status=404)
        case MultipleObjectsReturned():
            response = JsonResponse({'Error': 'Multiple objects returned'}, status=500)
        case UserEmailNotActivated():
            response = JsonResponse({'Error': str(exc)}, status=403)
        case MaxNumberAuth():
            response = JsonResponse({'Error': str(exc)}, status=431)
        case FieldNotEditable():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case _:
            response = JsonResponse({'Error': 'Internal Server Error'}, status=500)
    
    return response


def room_custom_exception_handler(exc):
    """ Handles custom exceptions raise from room funcs, returning the proper status code and error message """

    match exc:
        case IllegalArgumentError():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case ObjectDoesNotExist():
            response = JsonResponse({'Error': str(exc)}, status=404)
        case MultipleObjectsReturned():
            response = JsonResponse({'Error': str(exc)}, status=500)
        case UserAlreadyInRoom():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case PasswordsDoNotMatch():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case UserIsNotInTheRoom():
            response = JsonResponse({'Error'}, status=400)
        case _:
            response = JsonResponse({'Error': 'Internal Server Error'}, status=500)
    return response


def stream_custom_exception_handler(exc):
    """ Handles exceptions raise from stream funcs, returns the proper code and error msg """

    match exc:
        case StreamAssignedRoomRequired():
            response = JsonResponse({'Error': str(exc)}, status=424)
        case StreamAlreadyAssigned():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case StreamInvalidLink():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case MultipleObjectsReturned():
            response = JsonResponse({'Error': str(exc)}, status=500)
        case ObjectDoesNotExist():
            response = JsonResponse({'Error': str(exc)}, status=404)
        case CommonException():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case _:
            response = JsonResponse({'Error': 'Internal Server Error'}, status=500)
    return response

def handle_response(status_code, message):
    """ Returns proper response data """

    # If the obj is type set return list(obj)
    if isinstance(message, set):
        return JsonResponse(data=list(message), status=status_code, safe=False)
    else:
        return JsonResponse(data=message, status=status_code, safe=False)

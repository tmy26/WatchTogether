from knox.models import AuthToken
from knox import crypto
from django.http import JsonResponse
from .exceptions import *
from email_validator import EmailNotValidError
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned


def findUser(token:str) -> object:
    user = None
    try:
        raw_token = token.split(' ')[1]
        token_obj = AuthToken.objects.filter(digest=crypto.hash_token(raw_token)).first()
        user = token_obj.user
    except Exception:
        return user
    return user


def custom_exception_handler(exc):
    """ Handles custom exceptions, returning the proper status code and error message """

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
        case UserPasswordsDoNotMatch():
            response = JsonResponse({'Error': str(exc)}, status=400)
        case EmailNotValidError():
            error = 'The provided email is in a bad format.'
            response = JsonResponse({'Error': error}, status=400)
        case ObjectDoesNotExist():
            response = JsonResponse({'Error': str(exc)}, status=404)
        case MultipleObjectsReturned():
            response = JsonResponse({'Error': 'Multiple objects returned'}, status=400)
        case UserEmailNotActivated():
            response = JsonResponse({'Error': str(exc)}, status=403)
        case MaxNumberAuth():
            response = JsonResponse({'Error': str(exc)}, status=431)
        case FieldNotEditable():
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

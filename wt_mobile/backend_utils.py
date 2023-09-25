from knox.models import AuthToken
from knox import crypto


def findUser(token:str) -> object:
    user = None
    try:
        raw_token = token.split(' ')[1]
        token_obj = AuthToken.objects.filter(digest=crypto.hash_token(raw_token)).first()
        user = token_obj.user
    except Exception:
        return user
    return user

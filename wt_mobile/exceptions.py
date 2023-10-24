from rest_framework.exceptions import APIException


class CommonException(Exception):
    pass


class EmailAlreadyUsed(Exception):
    pass


class UsernameAlreadyUsed(Exception):
    pass


class EmailWasNotProvided(Exception):
    pass


class UsernameTooShort(Exception):
    pass


class UserPasswordIsTooShort(Exception):
    pass


class UserPasswordsDoNotMatch(Exception):
    pass


class UserEmailNotActivated(Exception):
    pass


class MaxNumberAuth(Exception):
    pass


class FieldNotEditable(Exception):
    pass
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


class PasswordsDoNotMatch(Exception):
    pass


class UserEmailNotActivated(Exception):
    pass


class MaxNumberAuth(Exception):
    pass


class FieldNotEditable(Exception):
    pass

class IllegalArgumentError(Exception):
    pass


class UserAlreadyInRoom(Exception):
    pass


class UserIsNotInTheRoom(Exception):
    pass


class StreamAssignedRoomRequired(Exception):
    pass


class StreamAlreadyAssigned(Exception):
    pass


class StreamInvalidLink(Exception):
    pass


class UserAlreadyActivated(Exception):
    pass

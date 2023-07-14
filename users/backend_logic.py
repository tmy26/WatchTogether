#here the whole logic for user creation and bla bla bla is going to be implemented
from .models import User
from .validators import user_name_validator, first_name_validator, last_name_validator, password_validator, email_validator
from django.contrib.auth.hashers import make_password


def create_user(request) -> dict:
    """
    User register method
    """
    #data request
    user_name = request.data.get('user_name')
    email = request.data.get('email')
    password = request.data.get('password')
    password_check = request.data.get('password_check')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    #check if email & user_name are unique
    if User.objects.filter(email=email).exists():
        return {'Error': 'the email must be unique'}
    if User.objects.filter(user_name=user_name).exists():
        return {'Error': 'the username must be unique'}



    user_name_validator(user_name)
    first_name_validator(first_name)
    last_name_validator(last_name)
    password_validator(password, password_check)
    email_validator(email)

    # TODO: better regex to verify email, more password validations, put method for user, login method
    hashed_password = make_password(password)
    #user creation
    User.objects.create(
        user_name=user_name,
        email=email,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
    )
    return {'Sucess': 'asd'}
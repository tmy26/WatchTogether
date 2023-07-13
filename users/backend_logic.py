#here the whole logic for user creation and bla bla bla is going to be implemented
from .models import User
import re


def create_user(request) -> dict:
    """
    User register method
    """
    #data request
    user_name = request.data.get('user_name')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    #check if email & user_name are unique
    if User.objects.filter(email=email).exists():
        return {'Error': 'the email must be unique'}
    if User.objects.filter(user_name=user_name).exists():
        return {'Error': 'the username must be unique'}
    
    # password valiidations
    if len(password) < 8:
        return {'Error': 'the password cant be less then 8 chars'}
    if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email):
        return {'Error': 'the email is invalid'}
    # TODO: better regex to verify email, more password validations, put method for user, login method

    #user creation
    User.objects.create(
        user_name=user_name,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
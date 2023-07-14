#here the whole logic for user creation and bla bla bla is going to be implemented
from .models import User
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
    
    #validations
    if len(user_name) < 3:
       return {'Error': 'the username is too short'}
    if len(first_name) == 0:
        return {'Error': 'the name field cannot be empty'}
    if len(last_name) == 0:
        return {'Error': 'the last_name field cannot be empty'}

    
    if password != password_check:
        return {'Error': 'passwords do not match'}
    if len(password) < 6:
        return {'Error': 'the lenght of the password is too short'}

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
    return {'Sucess': 'successfully created user'}


def edit_user(request):
    user_name = request.data.get('user_name')
    email = request.data.get('email')
    password = request.data.get('password')
    password_check = request.data.get('password_check')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    new_user_conf = User.objects.filter


def delete_user_account(request):
    """
    Deletes user account based on the email
    """
    email = request.data.get('email')

    if email:
        try:
            User.objects.get(email=email).delete()
            return {'Success': 'account deletion was successful.'}
        except User.DoesNotExist:
            return {'Error': 'An account with that email does not exist'}
    else:
        return {'Error': 'the field cannot be blank'}

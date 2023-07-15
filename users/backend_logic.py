#here the whole logic for user creation and bla bla bla is going to be implemented
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

def create_user(request) -> dict:
    """
    User register method
    """
    #data request
    user_name = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_check = request.data.get('password_check')

    # TODO: validators for password
    hashed_password = make_password(password)
    #user creation
    User.objects.create(
        user_name=user_name,
        email=email,
        password=hashed_password,
    )
    return {'Sucess': 'successfully created user'}


def edit_user(request, username):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_check = request.data.get('password_check')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return {"message": "The username does not exist!"}
    
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if password and password_check is not None:
        if password == password_check:
            user.password = password
    user.save()
    

def delete_user_account(request, username):
    """
    Deletes user account based on the email
    """

    try:
        User.objects.get(username=username).delete()
        return {"Success": "account deletion was successful"}
    except User.DoesNotExist:
        return {"Error": "An account with that username does not exist"}
    


def user_authentification(request) -> dict:
    username = request.data.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return {"message:": "Invalid username. Please try again"}
    
    #generete a new token for the user and delete the old one if exists.
    try:
        token = Token.objects.get(user=user)
        token.delete()
    except Token.DoesNotExist:
        pass
    finally:
        token = Token.objects.create(user=user)
    user.save()

    return {"message":"Successful authentifacation"}
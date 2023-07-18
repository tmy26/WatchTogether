#here the whole logic for user creation and bla bla bla is going to be implemented
from django.contrib.auth.base_user import AbstractBaseUser
from .models import User
from django.contrib.auth.hashers import make_password
#newly added

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from watch_together.general_utils import get_loggers
dev_logger = get_loggers('users')

#dev_logger.error(msg='TEST MESSAGE')
#dev_logger.info(msg='this is used when the message is success')


def activateEmail(request, user, to_email):
    mail_subject = "Activate user account."
    message = render_to_string("account_activation_template.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(subject=mail_subject, body=message, to=[to_email])
    
    if email.send():
        print('Succes Email send')
    else:
        print('email not send')
        return {'Error': 'problem occured'}


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return {'Success': 'activation ok'}
    else:
        return {'Error': 'blbabal'}
    

def create_user(request) -> dict:
    """
    User register method
    """
    #data request
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_check = request.data.get('password_check')

    # TODO: validators for password
    hashed_password = make_password(password)
    #user creation
    user = User.objects.create(
        username=username,
        email=email,
        password=hashed_password,
        is_active=False
    )
    user.save()
    return activateEmail(request, user, email)


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
    activateEmail()
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
    
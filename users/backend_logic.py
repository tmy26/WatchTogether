from django.contrib.auth.hashers import make_password
#newly added
#TODO: return a view when account is activated!
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from watch_together.general_utils import get_loggers
from .tokens import account_activation_token
from .models import User

from django.shortcuts import render, redirect


dev_logger = get_loggers('users_dev')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        #get the username object
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        dev_logger.info(msg=f"A new account was activated!")
        return redirect("https://www.google.com/")
    else:
        dev_logger.error(msg="Error. A error occured while trying to activate the account.\n The possible reason is that the user's token has expired!\n For debugging: Traceback users, backend_logic, activate") 
        return redirect("https://www.google.com/")
    
def activateEmail(request, user, to_email):
    mail_subject = "Activate your account"
    message = render_to_string("account_activation_template.html",
    {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(subject=mail_subject, body=message, to=[to_email])
    send_email = email.send()
    if send_email:
        dev_logger.info(msg=f'An activataion email was sent to {to_email} ')
        return {'Success': 'An activation email was successfully sent. Please check your inbox!'}
    else:
        dev_logger.error(msg='Error. An error occured while trying to send email. Traceback file: function: activateEmail in file: backend_logic in app: users')
        return {'Error': 'A problem occured while trying to send email, please try again later!'}


def create_user(request) -> None:
    """
    User register method
    """
    #data request

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_check = request.data.get('password_check')
    #validators
    if len(password) < 8:
        return {'Error': 'the password is too short!'}
    if password != password_check:
        return {'Error': 'the passwords do not match!'}
    if User.objects.filter(username=username).exists():
        return {'Error': 'the username is already in use!'}

    hashed_password = make_password(password)
    #user creation
    user = User.objects.create(
        username=username,
        email=email,
        password=hashed_password,
        is_active=False
    )
    dev_logger.info(msg=f"Account with username: {username} was created. The account is not yet activated!")
    activateEmail(request, user, email)
    return {'Activation': f'a verification email was sent to {email}'}


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
        return {"Error": "a account with that username does not exist"}
    
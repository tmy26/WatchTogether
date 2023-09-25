from django.core.mail import EmailMessage
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, login, authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from django.template.loader import render_to_string
from watch_together.general_utils import get_loggers
from email_validator import validate_email, EmailNotValidError
from knox.models import AuthToken
from .tokens import account_activation_token
from .models import User
from .serializers import UserSerializerSearchByUsername
from .backend_utils import findUser


dev_logger = get_loggers('dev_logger')
client_logger = get_loggers('client_logger')


def activate(request, uidb64, token) -> None:
    """Returns the token and redirects to url"""
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        # get the username object
        user = User.objects.get(pk=uid)
    except:
        user = None
        dev_logger.error('There is problem with token - activate function in backend_logic!')

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        client_logger.info(msg=f'A new account was activated!')
        return redirect("http://127.0.0.1:8000/account")
    else:
        dev_logger.error(msg='Error. A error occured while trying to activate the account.\n The possible reason is that the user token has expired!\n For debugging: Traceback wt_mobile, backend_logic, activate')
        return redirect("http://127.0.0.1:8000")
    
    
def activateEmail(request, user, to_email) -> None:
    """Sends email with verification link"""

    mail_subject = 'Activate your account'
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
        client_logger.info(msg=f'An activataion email was sent to {to_email} ')
    else:
        dev_logger.error(msg='Error. An error occured while trying to send email. Traceback file: function: activateEmail in file: backend_logic in app: wt_mobile')


def create_user(request) -> dict:
    """User register method"""

    # data request
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_check = request.data.get('password_check')
    
    # validate email uniqness
    if User.objects.filter(email=email).exists():
        return {'This email is already in use!'}
    # validate username uniqueness
    if User.objects.filter(username=username).exists():
        return {'Error': 'the username is already in use!'}
    # validate email len
    if len(str(email))==0:
        return {'Error': 'Email was not provided!'}
    # validate username len
    if len(username) <= 2:
        return {'Error', f'the username: {username} is too short'}
    # validate password
    if len(password) < 8:
        return {'Error': 'the password is too short!'}
    if password != password_check:
        return {'Error': 'the passwords do not match!'}

    # validate email
    try:
        check_email = validate_email(email, allow_smtputf8=False)
        if check_email:
            email = check_email.ascii_email
    except EmailNotValidError as error:
        client_logger.error(f'The provided email was invalid {email} !')
        return str(error)
    
    # convert the pass to hash
    hashed_password = make_password(password)

    # create user
    user = User(
        username=username,
        email=email,
        password=hashed_password,
        is_active=False
    )
    user.save()
    info = f'Account with username: {username} was created. The account is not yet activated!'
    client_logger.info(msg=info)
    activateEmail(request, user, email)
    return {'Activation': f'a verification email was sent to {email}'}
    

def get_user(request):
    """Get user's username"""
    username = request.data.get('username')

    try:
        user = User.objects.get(username=username)
        serialized = UserSerializerSearchByUsername(user)
    except User.DoesNotExist:
        return {'Error': 'The user does not exist!'}
    except MultipleObjectsReturned:
        dev_logger.error('Something is wrong with the db, function get_user in backend_logic has retuned two or more users with same username!')
        return {'Error': 'The user does not exist!'}
    return serialized


def login_user(request) -> dict:
    """Login method"""
    username = request.data.get('username')
    password = request.data.get('password')
    ERROR = {'Error': 'Invalid credintials!'}

    try:
        user_obj = User.objects.get(username=username)
    except MultipleObjectsReturned:
        dev_logger.error('Something is wrong with the db, function get_user in backend_logic has retuned two or more users with same username!')
        return ERROR
    except User.DoesNotExist:
        return ERROR

    if not user_obj.is_active:
        return {'Error': 'You must activate your email first and then login'}
    flag = authenticate(request, username=username, password=password)
    if flag:
        logged_devices = AuthToken.objects.filter(user=user_obj).count()
        if logged_devices >= 4:
            return {'Error': 'Maximum limit of logged devices is reached!'}
        token = AuthToken.objects.create(user_obj)
        print(token)
        login(request, flag)
        serialized = UserSerializerSearchByUsername(user_obj)
        return serialized
    else:
        return ERROR
    

def edit_profile(request) -> dict:
    """Edit profile method"""
    token = request.META.get('HTTP_AUTHORIZATION')
    user = findUser(token)
    method = 'password'
    #TODO: add request method func
    if user is None:
        return {'Error': 'User not found!'}
    else:
        match method:
            case 'password':
                password = request.data.get('password')
                password_check = request.data.get('password_check')
                # validate password
                if len(password) < 8:
                    return {'Error': 'the password is too short!'}
                if password != password_check:
                    return {'Error': 'the passwords do not match!'}
                user.set_password(password)
                user.save()
                client_logger.info(f'{user.username} has changed his password!')
                return {'Successs': 'Password changed successfully!'}
            case 'email':
                email = request.data.get('email')
                if User.objects.filter(email=email).exists():
                    return {'This email is already in use!'}
                # validate email len
                if len(str(email))==0:
                    return {'Error': 'Email was not provided!'}
                # validate email
                try:
                    check_email = validate_email(email, allow_smtputf8=False)
                    if check_email:
                        email = check_email.ascii_email
                except EmailNotValidError as error:
                    client_logger.error(f'The provided email was invalid {email} !')
                    return str(error)
                user.email=email
                user.save()
                client_logger.info(f'{user.username} has changed his email!')
                return {'Successs': 'Email changed successfully!'}
            case _:
                return {'Error': 'Please select what you want to edit!'}
                

def delete_profile(request) -> dict:
    """Delete profile method"""
    token = request.META.get('HTTP_AUTHORIZATION')
    user = findUser(token)
    
    if user is None:
        return {'Error': 'User not found!'}
    else:
        username = user.username
        User.objects.filter(username=username).delete()
        client_logger.info(f'{user.username} has deleted his account!')
        return {'Success': 'You have successfully deleted your account!'}
    

#TODO: return a view when account is activated!
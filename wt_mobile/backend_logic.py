from django.core.mail import EmailMessage
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, login, authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from watch_together.general_utils import get_loggers
from email_validator import validate_email, EmailNotValidError
from knox.models import AuthToken
from .tokens import account_activation_token
from .models import User
from .serializers import UserSerializerSearchByUsername, UserSerializerCheckIfUserActive
from .backend_utils import findUser
from django.shortcuts import render


dev_logger = get_loggers('dev_logger')
client_logger = get_loggers('client_logger')


def activate(request, uidb64, token) -> None:
    """ Activates account, sets field is_active to True """
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
        return render(request, 'activated_account_page.html')
    else:
        dev_logger.error(msg='Error. A error occured while trying to activate the account.\n The possible reason is that the user token has expired!\n For debugging: Traceback wt_mobile, backend_logic, activate')
        return render(request, 'activation_page_something_went_wrong.html')
    
    
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
        return {'Error': 'This email is already in use!'}
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
    """Login method, returns the header token"""
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
        login(request, flag)

        # returning username and token, so they can be stored as encrypted preferences in android
        user_info = {'username': f'{user_obj.username}', 'token': f'{token[1]}'}

        return user_info
    else:
        return ERROR
    

def edit_profile(request) -> dict:
    """Edit profile method"""
    token = request.META.get('HTTP_AUTHORIZATION')
    user = findUser(token)

    if user is None:
        return {'Error': 'User not found!'}
    else:
        # which field should be edited
        field = edit_method(request)

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_check = request.data.get('new_password_check')

        match field:
            case "email":
                new_email = request.data.get('new_email')

                if User.objects.filter(email=new_email).exists():
                    return {'This email is already in use!'}

                # validate data
                try:
                    validate_email(new_email)
                except EmailNotValidError as e:
                    client_logger.info('Provided email is not valid, details: ', e)
                    return {'Error': 'Provided email is not valid'}
                else:
                    client_logger.info(f'Email of {user.username} was changed')
                    user.save()
                    return {'Success': 'Email changed'}
            case "password":
                if user.password != make_password(old_password):
                    return {'Error': 'Old password do not match'}
                if len(new_password) < 8:
                    return {'Error': 'New password is too short'}
                if new_password != new_password_check:
                    return {'Error': 'Passwords do not match'}
                
                user.password = make_password(new_password)
                user.save()
                client_logger.info(f'{user.username} has changed its password')
                return {'Success': 'Password changed'}
            case _:
                return {'Error': 'Something went wrong'}


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


def is_user_active(request):
    """Checks if user is active"""

    username = request.data.get('username')

    try:
        user = User.objects.get(username=username)
        serialized = UserSerializerCheckIfUserActive(user)
    except User.DoesNotExist:
        return {'Error': 'User does not exist!'}

    except MultipleObjectsReturned:
        dev_logger.error('Something is wrong with the db, function is_user_active in backend logic has returned more than one object')
        return {'Error': 'The user does not exist!'}

    return serialized


def edit_method(request):
    """ Choose what user field will edit """

    field = request.data.get("field")

    if field != "password" and field != "email":
        return {'Error': 'Not editable field'}
    return field
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from email_validator import EmailNotValidError, validate_email
from knox.models import AuthToken
from watch_together.general_utils import get_loggers
from .backend_utils import findUser
from .exceptions import (CommonException, EmailAlreadyUsed,
                         EmailWasNotProvided, FieldNotEditable, MaxNumberAuth,
                         PasswordsDoNotMatch, UserEmailNotActivated,
                         UsernameAlreadyUsed, UsernameTooShort,
                         UserPasswordIsTooShort, UserAlreadyActivated)
from .models import User
from .serializers import (UserSerializerCheckIfUserActive,
                          UserSerializerSearchByUsername)
from .tokens import account_activation_token


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


def resend_activation_email(request):
    """ Sends an activation email again """

    username = request.data.get('username')

    try:
        # get user, its 'is_active' field should be 0, raise error if NOT
        user = User.objects.get(username=username)

        if user.is_active:
            raise UserAlreadyActivated('The user is already activated!')
        
        email = user.email

        # resend email
        activateEmail(request, user, to_email=email)

    except User.DoesNotExist:
        raise ObjectDoesNotExist('User is not found')
    except MultipleObjectsReturned:
        dev_logger.error('Something is wrong with the db, function get_user in backend_logic has retuned two or more users with same username!')
        raise MultipleObjectsReturned
    
    return {'Activation': f'A new verification email was sent to {email}'}


def create_user(request) -> dict:
    """User register method"""

    # data request
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_check = request.data.get('password_check')
    
    # validate email uniqness
    if User.objects.filter(email=email).exists():
        raise EmailAlreadyUsed('This email is already in use!')

    # validate username uniqueness
    if User.objects.filter(username=username).exists():
        raise UsernameAlreadyUsed('The username is already in use!')

    # validate email len
    if len(str(email))==0:
        raise EmailWasNotProvided('Email was not provided')

    # validate username len
    if len(username) <= 2:
        raise UsernameTooShort('Username is too short')

    # validate password
    if len(password) < 8:
        raise UserPasswordIsTooShort('The provided password is too short')

    if password != password_check:
        raise PasswordsDoNotMatch('The passwords do not match!')

    # validate email
    try:
        check_email = validate_email(email, allow_smtputf8=False)
        if check_email:
            email = check_email.ascii_email
    except EmailNotValidError:
        client_logger.error(f'The provided email was invalid {email} !')
        raise EmailNotValidError
    
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
        dev_logger.error('User is not found, traceback get_user in backend_logic')
        raise ObjectDoesNotExist('User not found!')

    except MultipleObjectsReturned:
        dev_logger.error('Something is wrong with the db, function get_user in backend_logic has retuned two or more users with same username!')
        raise MultipleObjectsReturned
    return serialized


def login_user(request) -> dict:

    """Login method, returns the header token"""
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user_obj = User.objects.get(username=username)
    except MultipleObjectsReturned:
        dev_logger.error('Something is wrong with the db, function get_user in backend_logic has retuned two or more users with same username!')
        raise MultipleObjectsReturned
    except User.DoesNotExist:
        dev_logger.error('User is not found, traceback login_user in backend_logic')
        raise ObjectDoesNotExist('User not found!')

    if not user_obj.is_active:
        raise UserEmailNotActivated('User email is not activated!')
    
    if check_password(password, user_obj.password):
        flag = authenticate(request, username=username, password=password)
        if flag:
            logged_devices = AuthToken.objects.filter(user=user_obj).count()
            if logged_devices >= 4:
                raise MaxNumberAuth('Maximum limit of logged devices is reached!')

            token = AuthToken.objects.create(user_obj)
            login(request, flag)

            # returning username and token, so they can be stored as encrypted preferences in android
            user_info = {'username': f'{user_obj.username}', 'token': f'{token[1]}'}

            return user_info
        else:
            dev_logger.error('Something went wrong, trace login_user()')
            raise CommonException()
    else:
        raise PasswordsDoNotMatch('Invalid user password!')
    

def edit_profile(request) -> dict:
    """Edit profile method"""
    token = request.META.get('HTTP_AUTHORIZATION')
    user = findUser(token)

    if user is None:
        raise ObjectDoesNotExist('User not found!')
    else:
        # which field should be edited
        field = edit_method(request)

        old_password = request.data.get('old_password')
        
        match field:
            case "email":
                new_email = request.data.get('new_email')

                if User.objects.filter(email=new_email).exists():
                    raise EmailAlreadyUsed('This email is already in use!')

                # validate data
                try:
                    if check_password(old_password, user.password):
                        validate_email(new_email)
                        user.email = new_email
                        client_logger.info(f'Email of {user.username} was changed')
                        user.save()
                        return {'Success': 'Email changed'}
                    else:
                        client_logger.info(f'Old passwords do not match')
                        raise PasswordsDoNotMatch('The passwords do not match!')
                except EmailNotValidError as e:
                    client_logger.info('Provided email is not valid, details: ', e)
                    raise EmailNotValidError

            case "password":
                new_password = request.data.get('new_password')
                new_password_check = request.data.get('new_password_check')

                if not check_password(old_password, user.password):
                    raise PasswordsDoNotMatch('Old password do not match!')
                if len(new_password) < 8:
                    raise UserPasswordIsTooShort('The provided password is too short')
                if new_password != new_password_check:
                    raise PasswordsDoNotMatch('The passwords do not match!')
                
                user.password = make_password(new_password)
                user.save()
                client_logger.info(f'{user.username} has changed its password')
                return {'Success': 'Password changed'}
            case _:
                raise CommonException()


def delete_profile(request) -> dict:
    """Delete profile method"""

    token = request.META.get('HTTP_AUTHORIZATION')
    user = findUser(token)
    
    if user is None:
        raise ObjectDoesNotExist('User not found!')
    else:
        username = user.username
        User.objects.filter(username=username).delete()
        client_logger.info(f'{user.username} has deleted his account!')
        return {'Success': 'You have successfully deleted your account!'}


def is_user_active(request):
    """Checks if user is active"""

    # get username from parameters
    username = request.GET.get('username')

    try:
        user = User.objects.get(username=username)
        serialized = UserSerializerCheckIfUserActive(user)
    except User.DoesNotExist:
        raise ObjectDoesNotExist('User not found!')

    except MultipleObjectsReturned:
        dev_logger.error('Something is wrong with the db, function is_user_active in backend logic has returned more than one object')
        raise MultipleObjectsReturned

    return serialized


def edit_method(request):
    """ Choose what user field will edit """

    field = request.data.get("field")

    if field != "password" and field != "email":
        raise FieldNotEditable('Not editable field!')
    return field
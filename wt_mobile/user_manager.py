from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from email_validator import EmailNotValidError, validate_email
from knox.models import AuthToken
from watch_together.general_utils import get_loggers
from .utils import UserUtils
from .exceptions import *
from .models import User
from .serializers import UserSerializerCheckIfUserActive, UserSerializerSearchByUsername
from .tokens import account_activation_token


dev_logger = get_loggers('dev_logger')
client_logger = get_loggers('client_logger')


def activate(request, uidb64, token) -> None:
    """
    Activates account, sets field is_active to a specific account to True.
    :param uid64: check what is this
    :type uid64: check what is this
    :param token: check
    :type token: check
    :rType: html page
    :returns: renders a successful or unsuccessful activation page.
    """
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        # get the username object
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
        dev_logger.error('There is problem with token - activate function in backend_logic!', exc_info=True)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        dev_logger.info(msg=f"A new account was activated!")
        return redirect("http://127.0.0.1:8000/activated_account_page.html")
    else:
        dev_logger.error(msg="Error. A error occured while trying to activate the account.\n The possible reason is that the user's token has expired!\n For debugging: Traceback users, backend_logic, activate") 
        return redirect("https://github.com/tmy26/WatchTogether")


def update_password(request, uidb64, token) -> None:
    """
    Activates account, sets field is_active to a specific account to True.
    :param uid64: check what is this
    :type uid64: check what is this
    :param token: check
    :type token: check
    :rType: html page
    :returns: renders a successful or unsuccessful activation page.
    """
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        # get the username object
        user = User.objects.get(pk=uid)
    except:
        user = None
        dev_logger.error('There is problem with token - activate function in backend_logic!')

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = False
        user.save()
        dev_logger.info(msg=f"A new account was activated!")
        return redirect("https://github.com/tmy26/WatchTogether")
    else:
        dev_logger.error(msg="Error. A error occured while trying to activate the account.\n The possible reason is that the user's token has expired!\n For debugging: Traceback users, backend_logic, activate") 
        return redirect("https://github.com/tmy26/WatchTogether")




class UserManager(object):
    """This class contains the following operations for Users(accounts):
    1. Create account
    2. Get specific account
    3. Login user into the website
    4. Edit user's account password
    5. Edit user's account email
    6. Delete user account
    7. Check if the user account status is_active = True
    8. Resend activation email
    """
    @classmethod
    def create_user_account(request) -> dict:
        """
        Creates user account.
        :param username: account username
        :type username: string
        :param email: account email
        :type email: string
        :param password: account password
        :type password: string
        :param password_check: retyping account password for verification
        :type password_check: string
        :rType: dict
        :returns: Message which indicates a successful registration.
        """
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
        UserUtils.send_email(request, mail_subject='Activate your account', template_path='account_activation_template.html', user=user, receiver=email)
        return {'Activation': f'a verification email was sent to {email}'}
    
    @staticmethod
    def get_user_account(request):
        """
        Searches account with specific username.
        :param username: account username
        :type username: string
        :rType: JSON serialized object
        :returns: Account username.
        """
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

    @staticmethod
    def login_user(request) -> dict:
        """
        Login method.
        :param username: account username
        :type username: string
        :rType: dictionary
        :returns: Account username with its token.
        """
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

    @staticmethod
    def edit_user_password(request):
        """
        Edits account password.
        :param token: the needed token to filter the user
        :type token: string
        :param new_password: the new password
        :type new_password: string
        :param new_password_check: used to verify new_password
        :type new_password_check: string
        :param current_password: the current password
        :type current_password: string
        :rType: dictionary
        :returns: Message which indicates a successful password change.
        """
        token = request.META.get('HTTP_AUTHORIZATION')
        new_password = request.data.get('new_password')
        new_password_check = request.data.get('new_password_check')
        current_password = request.data.get('password')
        user = UserUtils.findUser(token)

        if user is None:
            raise ObjectDoesNotExist('User not found!')
        else:
            if check_password(current_password, user.password):
                if len(new_password) < 8:
                    raise UserPasswordIsTooShort('The provided password is too short')
                if new_password != new_password_check:
                    raise PasswordsDoNotMatch('The passwords do not match!')
                            
                user.password = make_password(new_password)
                user.save()
                client_logger.info(f'An account with {user.username} has changed his password')
                return {'Success': 'Password changed'}
            else:
                msg = 'Old passwords do not match!'
                client_logger.info(msg=msg)
                raise PasswordsDoNotMatch(msg)

    @staticmethod
    def edit_user_email(request):
        """
        Changes account email.
        :param token: the needed token to filter the user
        :type token: string
        :param new_email: the new email that is going to used
        :type new_email: strin
        :param current_password: the current password
        :type current_password: string
        :rType: dictionary
        :returns: Message which indicates a successful email change.
        """
        token = request.META.get('HTTP_AUTHORIZATION')
        new_email = request.data.get('email')
        current_password = request.data.get('password')
        user = UserUtils.findUser(token)
        
        if user is None:
            raise ObjectDoesNotExist('User not found!')
        else:
            if User.objects.filter(email=new_email).exists():
                raise EmailAlreadyUsed('This email is already in use!')
            # validate data
            try:
                if check_password(current_password, user.password):
                    validate_email(new_email)
                    user.email = new_email
                    user.save()
                    client_logger.info(f'Email of {user.username} was changed')
                    return {'Success': 'Email changed'}
                else:
                    msg = 'Old passwords do not match!'
                    client_logger.info(msg=msg)
                    raise PasswordsDoNotMatch(msg)
            except EmailNotValidError:
                client_logger.info('Provided email is invalid!')
                raise EmailNotValidError
    
    @staticmethod
    def delete_user_account(request) -> dict:
        """
        Account deletion.
        :param token: the needed token to filter the user
        :type token: string
        :param password: the current password
        :type password: string
        :rType: dictionary
        :returns: Message which indicates a successful account deletion.
        """
        token = request.META.get('HTTP_AUTHORIZATION')
        password = request.data.get('password')
        user = UserUtils.findUser(token)
        
        if user is None:
            raise ObjectDoesNotExist('User not found!')
        else:
            if check_password(password, user.password):
                username = user.username
                User.objects.filter(username=username).delete()
                client_logger.info(f'{user.username} has deleted his account!')
                return {'Success': 'You have successfully deleted your account!'}

    @staticmethod
    def is_user_active(request):
        """
        Checks if user is active.
        :param username: a username
        :type username: string
        :rType: JSON serialized object
        :returns: Information about whether the user is active or not.
        """
        # get username from parameters
        username = request.GET.get('username')

        try:
            user = User.objects.get(username=username)
            serialized = UserSerializerCheckIfUserActive(user)
        except User.DoesNotExist:
            raise ObjectDoesNotExist('User not found!')

        except MultipleObjectsReturned:
            dev_logger.error('Something is wrong with the db, function is_user_active in backend logic has returned more than one object', exc_info=True)
            raise MultipleObjectsReturned

        return serialized
    #not finished yet
    @classmethod
    def reset_password(request):
        email = request.data.get('email')
        try:
            check_email = validate_email(email, allow_smtputf8=False)
            if check_email:
                email = check_email.ascii_email
        except EmailNotValidError:
            client_logger.error(f'The provided email was invalid {email} !')
            raise EmailNotValidError
        
        try:
            user = User.objects.get(email=email)
            UserUtils.send_email(request, mail_subject='Password reset', template_path='account_password_reset_template.html', user=user, receiver=email)
            
        except User.DoesNotExist:
            raise ObjectDoesNotExist('User not found!')
        except MultipleObjectsReturned:
            raise MultipleObjectsReturned('Something is wrong with the db, function password1 in backend logic has returned more than one object', exc_info=True)
        except Exception:
            raise CommonException(f'Something went wrong while trying to reset the password for user with username {user.username}', exc_info=True)

    @classmethod
    def resend_activation_email(cls, request) -> dict:
        """
        Resends activation email.
        :param username: account username
        :type username: string
        :rType: dictionary
        :returns: Message informing that the actiovation email was resend.
        """
        username = request.data.get('username')

        try:
            # get user, its 'is_active' field should be 0, raise error if NOT
            user = User.objects.get(username=username)

            if user.is_active:
                raise UserAlreadyActivated('The user is already activated!')
            
            email = user.email
            # resend email
            UserUtils.send_email(request, mail_subject='Activate your account', template_path='account_activation_template.html', user=user, receiver=email)
            return {'Activation': f'A new verification email was sent to {email}'}
        except User.DoesNotExist:
            raise ObjectDoesNotExist('User is not found')
        except MultipleObjectsReturned:
            dev_logger.error('Something is wrong with the db, function get_user in backend_logic has retuned two or more users with same username!')
            raise MultipleObjectsReturned

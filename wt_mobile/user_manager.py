from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from email_validator import EmailNotValidError, validate_email
from knox.models import AuthToken
from watch_together.general_utils import get_loggers
from .utils import UserUtils
from .exceptions import *
from .models import User
from .serializers import UserSerializerCheckIfUserActive, UserSerializerSearchByUsername

dev_logger = get_loggers('dev_logger')


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
    @staticmethod
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
        password_check = request.data.get('password check')
        
        # validate email uniqness
        if User.objects.filter(email=email).exists():
            raise EmailAlreadyUsed('This email is already in use!')
        # validate username uniqueness
        if User.objects.filter(username=username).exists():
            raise UsernameAlreadyUsed('The username is already in use!')
        # validate email len
        if len(str(email))==0:
            raise EmailWasNotProvided('Email was not provided!')
        # validate username len
        if len(username) <= 2:
            raise UsernameTooShort('Username is too short!')
        # validate password
        if len(password) < 8:
            raise UserPasswordIsTooShort('The provided password is too short!')
        if password != password_check:
            raise PasswordsDoNotMatch('The passwords do not match!')
        # validate email
        try:
            check_email = validate_email(email, allow_smtputf8=False)
            if check_email:
                email = check_email.ascii_email
        except EmailNotValidError:
            raise EmailNotValidError('The provided email is invalid!')
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
        UserUtils.send_email(request, mail_subject='Activate your account', template_path='account_activation_template.html', user=user, receiver=email)
        return {'Success': f'A verification email was sent to {email} !'}
    
    @staticmethod
    def get_user_account(request):
        """
        Searches account with specific username.
        :param username: account username
        :type username: string
        :rType: JSON serialized object
        :returns: Account username.
        """

        token = request.META.get('HTTP_AUTHORIZATION')
        user = UserUtils.findUser(token)

        try:
            user = User.objects.get(username=user.username)
            serialized = UserSerializerSearchByUsername(user)
            return serialized
        except User.DoesNotExist:
            raise ObjectDoesNotExist('Sorry, we could not find the user you are looking for!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the get_user_account process in user_manager.py!'
            raise MultipleObjectsReturned(error_msg)
        
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
            error_msg = 'An issue with the database: Multiple objects were returned during the login_user process in user_manager.py!'
            dev_logger.error(error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)
        except User.DoesNotExist:
            raise ObjectDoesNotExist('Sorry, we could not find an account matching these credentials!')

        if not user_obj.is_active:
            raise UserEmailNotActivated('Please activate your email. The verification is still pending.')
        
        flag = authenticate(request, username=username, password=password)

        if flag:
            logged_devices = AuthToken.objects.filter(user=user_obj).count()
            if logged_devices >= 4:
                raise MaxNumberAuth('Maximum limit of logged devices is reached!')
            token = AuthToken.objects.create(user_obj)
            login(request, flag)
            user_info = {'username': f'{user_obj.username}', 'token': f'{token[1]}'}
            return user_info
        else:
            raise PasswordsDoNotMatch('Invalid user password!')

    @staticmethod
    def edit_user_password(request) -> dict:
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
        new_password = request.data.get('new password')
        new_password_check = request.data.get('new password check')
        current_password = request.data.get('current password')
        user = UserUtils.findUser(token)

        if user is None:
            raise ObjectDoesNotExist('Sorry, something went wrong. Please try to logut and login again!')
        else:
            if check_password(current_password, user.password):
                if len(new_password) < 8:
                    raise UserPasswordIsTooShort('The provided password is too short!')
                if new_password != new_password_check:
                    raise PasswordsDoNotMatch('The passwords do not match!')
                user.password = make_password(new_password)
                user.save()
                return {'Success': 'Password successfully changed!'}
            else:
                raise PasswordsDoNotMatch('Old passwords do not match!')

    @staticmethod
    def edit_profile(request) -> dict:
        """
        Changes account email or password.
        :param token: the needed token to filter the user
        :type token: string
        :param field_to_change: Which field to change - "email" or "password"
        :type field_to_change: String
        :param new_email: the new email that is going to used
        :type new_email: String
        :param user_password: the current user password
        :type user_password: string
        :param new_password
        :type new_password: String
        :rType: dictionary
        :returns: Message which indicates a field has been changed.
        """
        token = request.META.get('HTTP_AUTHORIZATION')
        # field_to_change = request.data.get('field_to_change')
        # currently is hardcoded bcs we all lazy and being able to change password only is enought for now
        field_to_change = "password"
        user_password = request.data.get('user_password')

        user = UserUtils.findUser(token)
        
        if user is None:
            raise ObjectDoesNotExist('Sorry, something went wrong. Please try to logut and login again!')
        else:
            match field_to_change:
                case "email":
                    # check if current passwords match
                    if check_password(user_password, user.password):
                        new_email = request.data.get('new_email')

                        if User.objects.filter(email=new_email).exists():
                            raise EmailAlreadyUsed('This email is already in use!')
                        # validate email
                        try:
                            check_email = validate_email(new_email, allow_smtputf8=False)
                            if check_email:
                                new_email = check_email.ascii_email
                        except EmailNotValidError:
                            raise EmailNotValidError('The provided email is invalid!')
                        
                        user.email = new_email
                        user.save()
                        return {'Success': f'The email associated with {user.username} has been changed!'}
                    else:
                        raise PasswordsDoNotMatch('The current password of the account does not match the provided one!')
                                 
                case "password":
                    if check_password(user_password, user.password):
                        new_password = request.data.get('new_password')

                        # validate password same validation as when creating the user
                        if len(new_password) < 8:
                            raise UserPasswordIsTooShort('The provided password is too short!')
                        if check_password(new_password, user.password):
                            raise PasswordsDoNotMatch('Newly provided password is the same as the current password.')
                        
                        hashed_password = make_password(new_password)

                        user.password = hashed_password
                        user.save()
                        return {'Success': f'The password of {user.username} has been changed!'}
                    else:
                        raise PasswordsDoNotMatch('The current password of the account does not match the provided one!')
    
    @staticmethod
    def delete_user_account(request) -> dict:
        """
        Account deletion, removes the related auth tokens also.
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
            raise ObjectDoesNotExist('Sorry, something went wrong. Please try to logut and login again!')
        else:
            if check_password(password, user.password):
                username = user.username
                User.objects.filter(username=username).delete()
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
        username = request.GET.get('username')

        try:
            user = User.objects.get(username=username)
            serialized = UserSerializerCheckIfUserActive(user)
            return serialized
        except User.DoesNotExist:
            raise ObjectDoesNotExist('Sorry, we could not find the user you are looking for!')
        except MultipleObjectsReturned:
            error_msg='There is an issue with the database; the is_user_active method in user_manager.py has returned multiple objects!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)
        
    #not finished yet
    @classmethod
    def reset_password(request):
        email = request.data.get('email')

        try:
            check_email = validate_email(email, allow_smtputf8=False)
            if check_email:
                email = check_email.ascii_email
        except EmailNotValidError:
            raise EmailNotValidError(f'The provided email {email} is invalid!')
        
        try:
            user = User.objects.get(email=email)
            UserUtils.send_email(request, mail_subject='Password reset', template_path='account_password_reset_template.html', user=user, receiver=email)
            
        except User.DoesNotExist:
            raise ObjectDoesNotExist('User not found!')
        except MultipleObjectsReturned:
            error_msg = 'An issue with the database: Multiple objects were returned during the reset_password process in user_manager.py!'
            dev_logger.error(error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)
        except Exception:
            error_msg = f'Something went wrong while trying to reset the password for user with username {user.username}!'
            dev_logger.error(error_msg, exc_info=True)
            raise CommonException(error_msg)

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
                raise UserAlreadyActivated(f'The account {user.username} is already activated!')
            
            email = user.email
            UserUtils.send_email(request, mail_subject='Activate your account', template_path='account_activation_template.html', user=user, receiver=email)
            return {'Activation': f'A new verification email has been sent to {email}'}
        except User.DoesNotExist:
            raise ObjectDoesNotExist(f'Sorry, the acccount with {username} does not exist!')
        except MultipleObjectsReturned:
            error_msg='An issue with the database: Multiple objects were returned during the resend_activation_email process in user_manager.py!'
            dev_logger.error(msg=error_msg, exc_info=True)
            raise MultipleObjectsReturned(error_msg)

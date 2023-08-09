from django.core.mail import EmailMessage
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from django.template.loader import render_to_string
from watch_together.general_utils import get_loggers
from email_validator import validate_email, EmailNotValidError
from .tokens import account_activation_token
from .models import User
from .serializers import UserSerializerSearchByUsername


dev_logger = get_loggers('wt_mobile_dev')


def activate(request, uidb64, token):
    """Returns the token and redirects to url"""
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
        dev_logger.info(msg=f'A new account was activated!')
        return redirect("https://github.com/tmy26/WatchTogether")
    else:
        dev_logger.error(msg='Error. A error occured while trying to activate the account.\n The possible reason is that the user token has expired!\n For debugging: Traceback wt_mobile, backend_logic, activate')
        return redirect("https://github.com/tmy26/WatchTogether")
    
    
def activateEmail(request, user, to_email):
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
        dev_logger.info(msg=f'An activataion email was sent to {to_email} ')
    else:
        dev_logger.error(msg='Error. An error occured while trying to send email. Traceback file: function: activateEmail in file: backend_logic in app: wt_mobile')


def create_user(request) -> None:
    """User register method"""

    #data request
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_check = request.data.get('password_check')

    #validate email and check for uniqness
    try:
        check_email = validate_email(email, check_deliverability=True)
        email = check_email.normalized
    except EmailNotValidError as error:
        return str(error)
    
    if User.objects.filter(email=email).exists():
        return {'This email is already in use!'}
    
    #validate password
    if len(password) < 8:
        return {'Error': 'the password is too short!'}
    if password != password_check:
        return {'Error': 'the passwords do not match!'}
    
    #validate user_uniqueness
    if User.objects.filter(username=username).exists():
        return {'Error': 'the username is already in use!'}
    
    #convert the pass to hash
    hashed_password = make_password(password)

    #create user
    user = User(
        username=username,
        email=email,
        password=hashed_password,
        is_active=False
    )
    # user.groups.add(USER_GROUP) // Still wondering if we are going to use groups for permissions
    user.save()
    dev_logger.info(msg=f'Account with username: {username} was created. The account is not yet activated!')
    activateEmail(request, user, email)
    return {'Activation': f'a verification email was sent to {email}'}
    

def get_user(request):
    """Get user's username"""
    username = request.data.get('username')

    try:
        user = User.objects.get(username=username)
        serialized = UserSerializerSearchByUsername(user)
    except (User.DoesNotExist, MultipleObjectsReturned):
        return {'Error': 'The user does not exist!'}
    return serialized

#TODO: return a view when account is activated!
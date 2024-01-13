from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from watch_together.general_utils import get_loggers
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
        return redirect("https://github.com/tmy26/WatchTogether")
    else:
        dev_logger.error(msg="Error. A error occured while trying to activate the account.\n The possible reason is that the user's token has expired!\n For debugging: Traceback special_functions.py - activate method") 
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

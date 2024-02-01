from django.urls import path
from knox import views as knox_views
from wt_mobile.special_functions import activate
from wt_mobile.views import (RoomExtendedView, RoomView, StreamView, UserLogin,
                             UserProfile, UserView, ResendActivationEmailView, PasswordView)


urlpatterns = [
    path('user/register', UserView.as_view()),
    path('user/resend_email', ResendActivationEmailView.as_view()),
    path('login', UserLogin.as_view()),
    path('account', UserProfile.as_view()),
    path('room', RoomView.as_view(), name='room'),
    path('room/extended_view', RoomExtendedView.as_view()),
    path('stream', StreamView.as_view()),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('logout',knox_views.LogoutView.as_view(), name='knox-logout'),
    path('logoutall',knox_views.LogoutAllView.as_view(), name='knox-logout-all'),
    path('password_reset', PasswordView.as_view()),

]
    # path('password/<uidb64>/<token>', resend_password, name='password'),
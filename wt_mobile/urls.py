from django.urls import path
from wt_mobile.views import StreamView, RoomView, UserView, UserLogin, UserProfile, RoomExtendedView
from knox import views as knox_views
from wt_mobile.backend_logic import activate


urlpatterns = [
    path('user/register', UserView.as_view()),
    path('login', UserLogin.as_view()),
    path('account', UserProfile.as_view()),
    path('room', RoomView.as_view()),
    path('room/extended_view', RoomExtendedView.as_view()),
    path('stream', StreamView.as_view()),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('logout',knox_views.LogoutView.as_view(), name='knox-logout'),
    path('logoutall',knox_views.LogoutAllView.as_view(), name='knox-logout-all'),
]

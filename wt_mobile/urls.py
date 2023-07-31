from django.urls import path
from .views import UserRegistration, EditUser, RoomCreationView, StreamCreation
from . import backend_logic


urlpatterns = [
    path('user_registration', UserRegistration.as_view()),
    path('user_edit', EditUser.as_view()),
    path('room_creation', RoomCreationView.as_view()),
    path('activate/<uidb64>/<token>', backend_logic.activate, name='activate'),
    path('stream_creation', StreamCreation.as_view())
]

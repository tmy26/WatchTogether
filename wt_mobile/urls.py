from django.urls import path
from .views import UserRegistrationView, EditUserView, RoomCreationView, StreamCreationView, JoinRoomView
from . import backend_logic


urlpatterns = [
    path('user_registration', UserRegistrationView.as_view()),
    path('user_edit', EditUserView.as_view()),
    path('room_creation', RoomCreationView.as_view()),
    path('activate/<uidb64>/<token>', backend_logic.activate, name='activate'),
    path('stream_creation', StreamCreationView.as_view()),
    path('room_joining', JoinRoomView.as_view())
]

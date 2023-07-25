from django.urls import path
from .views import UserRegistration, UserAuthentification, RoomCreation , StreamCreation


urlpatterns = [
    path('user_registration', UserRegistration.as_view()),
    path('user_authentification', UserAuthentification.as_view()),
    path('room_creation', RoomCreation.as_view()),
    path('stream_creation', StreamCreation.as_view())
]

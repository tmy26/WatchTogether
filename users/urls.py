from django.urls import path
from .views import UserRegistration, RoomCreation

urlpatterns = [
    path('user_registration', UserRegistration.as_view()),
    path('room_creation', RoomCreation.as_view()),
]
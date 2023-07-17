from django.urls import path
<<<<<<< HEAD
from .views import UserRegistration, UserAuthentification

urlpatterns = [
    path('user_registration', UserRegistration.as_view()),
    path('user_authentification', UserAuthentification.as_view())
=======
from .views import UserRegistration, RoomCreation

urlpatterns = [
    path('user_registration', UserRegistration.as_view()),
    path('room_creation', RoomCreation.as_view()),
>>>>>>> main
]
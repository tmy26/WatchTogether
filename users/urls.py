from django.urls import path
from .views import UserRegistration

urlpatterns = [
    path('user_registration', UserRegistration.as_view()),
]
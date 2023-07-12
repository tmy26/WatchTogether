from django.urls import path
from .views import UserRegistration

urlpatterns = [
    path('', UserRegistration.as_view()),
]
# Spring-like request mappings for djnago. All urls are registered in the project url.py

from django.urls import path
from wt_mobile import backend_logic
from django.contrib import admin


urlpatterns = [
    path('activate/<uidb64>/<token>', backend_logic.activate, name='activate')
]

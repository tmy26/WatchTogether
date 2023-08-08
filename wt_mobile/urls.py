# Spring-like request mappings for djnago. All urls are defined in the main url.py

from django.urls import path
from wt_mobile import backend_logic


urlpatterns = [
    path('activate/<uidb64>/<token>', backend_logic.activate, name='activate')
]

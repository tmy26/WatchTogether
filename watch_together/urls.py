from django.urls import path, include
from wt_mobile import backend_logic
from django.contrib import admin


urlpatterns = [
    path('', include('wt_mobile.urls')),
    path('admin/', admin.site.urls)
]

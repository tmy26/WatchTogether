from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('', include('wt_mobile.urls')),
    path('admin/', admin.site.urls),
]

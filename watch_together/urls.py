from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('wt_mobile.urls') ),
]
#Deleted website paths from here and as app in settings, bcs we are going to use React for frontend
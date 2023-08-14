from django.urls import path, include
from wt_mobile.backend_logic import activate
from django.contrib import admin


urlpatterns = [
    path('', include('wt_mobile.urls')),
    path('admin/', admin.site.urls),
    path('activate/<uidb64>/<token>', activate, name='activate')
]

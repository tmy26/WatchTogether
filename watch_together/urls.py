from django.contrib import admin
from django.urls import include, path
from chat_app.routing import websocket_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wt_mobile.urls')),
    path('ws/', include(websocket_urlpatterns)),
]

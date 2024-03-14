from django.contrib import admin
from django.urls import include, path
from chat_app.routing import websocket_urlpatterns
from chat_app.views import MessageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('wt_mobile.urls')),
    path('ws/', include(websocket_urlpatterns)),
    path('chat/', MessageView.as_view(), name='chat'),
]

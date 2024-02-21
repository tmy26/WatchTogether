# chat_app/routing.py
from django.urls import re_path
from .consumers import ChatConsumer

# The WebSocket URL pattern for chat rooms is defined by this code
websocket_urlpatterns = [
    re_path(r'ws/chat_app/(?P<unique_id>\w+)/$', ChatConsumer.as_asgi()),

]

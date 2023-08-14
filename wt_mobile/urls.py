from wt_mobile.views import StreamView, RoomView, UserView
from django_request_mapping import UrlPattern
from .backend_logic import activate
from django.urls import path


urlpatterns = UrlPattern()
urlpatterns.register(UserView)
urlpatterns.register(StreamView)
urlpatterns.register(RoomView)

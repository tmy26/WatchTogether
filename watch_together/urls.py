from wt_mobile.views import StreamView, RoomView, UserView
from django_request_mapping import UrlPattern
from django.urls import path, include
from django.contrib import admin

urlpatterns = UrlPattern()

urlpatterns.register(UserView)
urlpatterns.register(StreamView)
urlpatterns.register(RoomView)

urlpatterns += [path('', include('wt_mobile.urls'))]
urlpatterns += [path('admin/', admin.site.urls)]

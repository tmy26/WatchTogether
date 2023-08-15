from wt_mobile.views import StreamView, RoomView, UserView
from django_request_mapping import UrlPattern


urlpatterns = UrlPattern()
urlpatterns.register(UserView)
urlpatterns.register(StreamView)
urlpatterns.register(RoomView)

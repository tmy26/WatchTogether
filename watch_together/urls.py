from wt_mobile.views import StreamView, RoomView, UserView
from django_request_mapping import UrlPattern

urlpatterns = UrlPattern()

urlpatterns.register(UserView)
#urlpatterns.register(backend_logic.activate) # TODO Fix the backend_logic.activate
urlpatterns.register(StreamView)
urlpatterns.register(RoomView)

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .backend_logic import delete_user_account, create_user, get_user
from .backend_logic_rooms import *
from .backend_logic_stream import *
from django_request_mapping import request_mapping
from django.http import JsonResponse


@request_mapping('/user')
class UserView(APIView):
    """ User Controller """

    @request_mapping('/register_user', method='post')
    def create(self, request):
        return handle_response(create_user(request))
    
    @request_mapping('/search_user', method='get')
    def get(self, request):
        return handle_response(get_user(request))

    @request_mapping('/delete_user', method='delete')
    def remove(self, request):
        return handle_response(delete_user_account(request))

# ---------End of User Controller--------- #


@request_mapping('/room')
class RoomView(APIView):
    """ Room Controller """
    permission_classes = [IsAuthenticated]

    @request_mapping('/create_room', method='post')
    def create(self, request):
        return handle_response(create_room(request))

    @request_mapping('/remove_room', method='delete')
    def delete(self, request):
        return handle_response(delete_room(request))

    @request_mapping('/edit_room', method='put')
    def edit(self, request):
        return handle_response(edit_room(request))

    @request_mapping('/list_rooms', method='get')
    def get(self, request):
        msg = list_rooms_user_participates(request)
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return JsonResponse(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data=msg.data, status=status.HTTP_200_OK, safe=False)

    @request_mapping('/join_room', method='post')
    def join(self, request):
        return handle_response(join_room(request))

    @request_mapping('/leave_room', method='delete')
    def leave(self, request):
        return handle_response(leave_room(request))

# ---------End of Room Controller--------- #


@request_mapping('/stream')
class StreamView(APIView):
    """ Stream Controller """

    @request_mapping('/create_stream', method='post')
    def create(self, request):
        return handle_response(create_steam(request))

    @request_mapping('/edit_stream', method='put')
    def edit(self, request):
        return handle_response(edit_stream(request))
    

# ---------End of Stream Controller--------- #


# ---------Support Functions--------- #

def handle_response(msg):
    if isinstance(msg, dict) and 'Error' in msg.keys():
        return JsonResponse(data=msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data=msg, status=status.HTTP_200_OK)

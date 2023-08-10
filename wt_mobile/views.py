from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .backend_logic import create_user, get_user
from .backend_logic_rooms import *
from .backend_logic_stream import *
from django_request_mapping import request_mapping
from django.http import JsonResponse


@request_mapping('/user')
class UserView(APIView):
    """ User Controller """

    @request_mapping('/register', method='post')
    def create(self, request):
        return handle_response(create_user(request))
    
    @request_mapping('/search', method='get')
    def get(self, request):
        msg = get_user(request)
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return JsonResponse(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data=msg.data, status=status.HTTP_200_OK, safe=False)

# ---------End of User Controller--------- #


@request_mapping('/room')
class RoomView(APIView):
    """ Room Controller """
    permission_classes = [IsAuthenticated]

    @request_mapping('/create', method='post')
    def create(self, request):
        return handle_response(create_room(request))

    @request_mapping('/remove', method='delete')
    def delete(self, request):
        return handle_response(delete_room(request))

    @request_mapping('/edit', method='put')
    def edit(self, request):
        return handle_response(edit_room(request))

    @request_mapping('/list', method='get')
    def get(self, request):
        msg = list_rooms_user_participates(request)
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return JsonResponse(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data=msg.data, status=status.HTTP_200_OK, safe=False)

    @request_mapping('/join', method='post')
    def join(self, request):
        return handle_response(join_room(request))

    @request_mapping('/leave', method='delete')
    def leave(self, request):
        return handle_response(leave_room(request))

# ---------End of Room Controller--------- #


@request_mapping('/stream')
class StreamView(APIView):
    """ Stream Controller """

    @request_mapping('/create', method='post')
    def create(self, request):
        return handle_response(create_steam(request))

    @request_mapping('/edit', method='put')
    def edit(self, request):
        return handle_response(edit_stream(request))
    

# ---------End of Stream Controller--------- #


# ---------Support Functions--------- #

def handle_response(msg):
    if isinstance(msg, dict) and 'Error' in msg.keys():
        return JsonResponse(data=msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        # If the obj is type set return list(obj)
        if isinstance(msg, set):
            return JsonResponse(data=list(msg), status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse(data=msg, status=status.HTTP_200_OK)

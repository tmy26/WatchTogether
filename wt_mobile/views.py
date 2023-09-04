from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .backend_logic import create_user, get_user, login_user, edit_profile, delete_profile
from .backend_logic_rooms import *
from .backend_logic_stream import *
from django_request_mapping import request_mapping
from django.http import JsonResponse
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication


@request_mapping('/user')
class UserView(APIView):
    """User register"""
    permission_classes = (AllowAny,)

    @request_mapping('/register', method='post')
    def create(self, request):
        return handle_response(create_user(request))
    

@request_mapping('/login')
class UserLogin(KnoxLoginView):
    """User login"""
    permission_classes = (AllowAny,)
    
    @request_mapping('', method='post')
    def signin(self, request):
        return handle_response_data(login_user(request))
    

@request_mapping('/account')
class UserProfile(APIView):
    """User S.E.D(search, edit, delete)"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @request_mapping('/edit', method='put')
    def edit_user(self, request):
        return handle_response(edit_profile(request))
        
    @request_mapping('/delete', method='delete')
    def delete_user(self, request):
        return handle_response(delete_profile(request))
        
    @request_mapping('/search', method='get')
    def get_user(self, request):
        return handle_response_data(get_user(request))


@request_mapping('/room')
class RoomView(APIView):
    """Room Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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
        return handle_response_data(list_rooms_user_participates(request))

    @request_mapping('/join', method='post')
    def join(self, request):
        return handle_response(join_room(request))

    @request_mapping('/leave', method='delete')
    def leave(self, request):
        return handle_response(leave_room(request))


@request_mapping('/stream')
class StreamView(APIView):
    """Stream Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @request_mapping('/create', method='post')
    def create(self, request):
        return handle_response(create_stream(request))

    @request_mapping('/edit', method='put')
    def edit(self, request):
        return handle_response(edit_stream(request))


# ---------Support Functions--------- #

def handle_response(msg):
    if isinstance(msg, dict) and 'Error' in msg.keys():
        return JsonResponse(data=msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        # If the obj is type set return list(obj)
        if isinstance(msg, set):
            return JsonResponse(data=list(msg), status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse(data=msg, status=status.HTTP_200_OK, safe=False)


def handle_response_data(msg):
    if isinstance(msg, dict) and 'Error' in msg.keys():
        return JsonResponse(data=msg, status=status.HTTP_200_OK, safe=False)
    else:
        return JsonResponse(msg.data, status=status.HTTP_200_OK)
    
#TODO: refactor views
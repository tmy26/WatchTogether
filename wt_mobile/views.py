from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .backend_logic import create_user, get_user, login_user, edit_profile, delete_profile, is_user_active
from .backend_logic_rooms import *
from .backend_logic_stream import *
from django.http import JsonResponse
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication



class UserView(APIView):
    """User register"""
    permission_classes = (AllowAny,)

    def post(self, request):
        return handle_response(create_user(request))
    
    def get(self, request):
        return handle_response_data(is_user_active(request))


class UserLogin(KnoxLoginView):
    """User login"""
    permission_classes = (AllowAny,)
    
    def post(self, request):
        return handle_response(login_user(request))
    

class UserProfile(APIView):
    """User S.E.D(search, edit, delete)"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request):
        return handle_response(edit_profile(request))
        
    def delete(self, request):
        return handle_response(delete_profile(request))
        
    def get(self, request):
        return handle_response_data(get_user(request))
    

class RoomView(APIView):
    """Room Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        return handle_response(create_room(request))

    def delete(self, request):
        return handle_response(delete_room(request))

    def put(self, request):
        return handle_response(edit_room(request))

    def get(self, request):
        return handle_response_data(list_rooms_user_participates(request))
    

class RoomExtendedView(APIView):
    """Room Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        return handle_response(join_room(request))

    def delete(self, request):
        return handle_response(leave_room(request))


class StreamView(APIView):
    """Stream Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        return handle_response(create_stream(request))

    def put(self, request):
        return handle_response(edit_stream(request))
    
    def get(self, request):
        return handle_response_data(display_history(request))


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
        return JsonResponse(data=msg, status=status.HTTP_400_BAD_REQUEST, safe=False)
    else:
        return JsonResponse(data=msg.data, status=status.HTTP_200_OK, safe=False)

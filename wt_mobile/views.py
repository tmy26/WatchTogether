from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .backend_logic import create_user, get_user, login_user, edit_profile, delete_profile, is_user_active
from .backend_logic_rooms import *
from .backend_logic_stream import *
from django.http import JsonResponse
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from .backend_utils import custom_exception_handler, handle_response


class UserView(APIView):
    """User register"""
    permission_classes = (AllowAny,)

    def post(self, request):

        # try creating the user, else return the appropriate exception
        try:
            message = create_user(request)
            status_code = status.HTTP_201_CREATED
            return handle_response(status_code, message)
        except Exception as e:
            return custom_exception_handler(e)
    
    def get(self, request):
        
        try:
            message = is_user_active(request)
            return JsonResponse(data=message.data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return custom_exception_handler(e)


class UserLogin(KnoxLoginView):
    """User login"""
    permission_classes = (AllowAny,)
    
    def post(self, request):
        try:
            message = login_user(request)
            status_code = 202
            return handle_response(status_code, message)
        except Exception as e:
            return custom_exception_handler(e)
    

class UserProfile(APIView):
    """User S.E.D(search, edit, delete)"""

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request):
        try:
            message = edit_profile(request)
            status_code = 200
            return handle_response(status_code, message)
        except Exception as e:
            return custom_exception_handler(e)

        
    def delete(self, request):
        try:
            message = delete_profile(request)
            status_code = 200
            return handle_response(status_code, message)
        except Exception as e:
            return custom_exception_handler(e)

        
    def get(self, request):

        # try getting the user, else return the appropriate exception
        try:
            message = get_user(request)
            return JsonResponse(data=message.data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return custom_exception_handler(e)
    

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

from django.http import JsonResponse
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .backend_logic import (create_user, delete_profile, edit_profile,
                            get_user, is_user_active, login_user, resend_activation_email)
from .backend_logic_rooms import *
from .backend_logic_stream import *
from .backend_utils import (handle_response, room_custom_exception_handler,
                            stream_custom_exception_handler,
                            user_custom_exception_handler)


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
            return user_custom_exception_handler(e)
    
    def get(self, request):
        
        try:
            message = is_user_active(request)
            return JsonResponse(data=message.data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return user_custom_exception_handler(e)


class ResendActivationEmailView(APIView):
    """ Currently only the resend activation email functionality """
    permission_classes = (AllowAny,)

    def post(self, request):

        # try resending email, else return appropriate exception
        try:
            message = resend_activation_email(request)
            status_code = status.HTTP_200_OK
            return handle_response(status_code, message)
        except Exception as e:
            return user_custom_exception_handler(e)


class UserLogin(KnoxLoginView):
    """User login"""
    permission_classes = (AllowAny,)
    
    def post(self, request):
        try:
            message = login_user(request)
            status_code = 202
            return handle_response(status_code, message)
        except Exception as e:
            return user_custom_exception_handler(e)
    

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
            return user_custom_exception_handler(e)

        
    def delete(self, request):
        try:
            message = delete_profile(request)
            status_code = 200
            return handle_response(status_code, message)
        except Exception as e:
            return user_custom_exception_handler(e)

        
    def get(self, request):

        # try getting the user, else return the appropriate exception
        try:
            message = get_user(request)
            return JsonResponse(data=message.data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return user_custom_exception_handler(e)
    

class RoomView(APIView):
    """Room Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            message = create_room(request)
            status_code = status.HTTP_201_CREATED
            return handle_response(status_code, message)
        except Exception as e:
            return room_custom_exception_handler(e)

    def delete(self, request):
        try:
            message = delete_room(request)
            status_code = status.HTTP_200_OK
            return handle_response(status_code, message)
        except Exception as e:
            return room_custom_exception_handler(e)

    def put(self, request):
        try:
            message = edit_room(request)
            status_code = status.HTTP_200_OK
            return handle_response(status_code, message)
        except Exception as e:
            return room_custom_exception_handler(e)

    def get(self, request):
        try:
            message = list_rooms_user_participates(request)
            return JsonResponse(data=message.data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return room_custom_exception_handler(e)
    

class RoomExtendedView(APIView):
    """Room Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            message = join_room(request)
            status_code = status.HTTP_200_OK
            return handle_response(status_code, message)
        except Exception as e:
            return room_custom_exception_handler(e)

    def delete(self, request):
        try:
            message = leave_room(request)
            status_code = status.HTTP_200_OK
            return handle_response(status_code, message)
        except Exception as e:
            return room_custom_exception_handler(e)
    

class StreamView(APIView):
    """Stream Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            message = create_stream(request)
            status_code = status.HTTP_201_CREATED
            return handle_response(status_code, message)
        except Exception as e:
            stream_custom_exception_handler(e)

    def put(self, request):
        try:
            message = edit_stream(request)
            status_code = status.HTTP_200_OK
            return handle_response(status_code, message)
        except Exception as e:
            stream_custom_exception_handler(e)
    
    def get(self, request):
        try:
            message = display_history(request)
            return JsonResponse(data=message.data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return room_custom_exception_handler(e)

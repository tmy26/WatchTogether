from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .user_manager import UserManager
from .room_manager import RoomManager
from .stream_manager import StreamManager
from .utils import HandleResponseUtils, CustomExceptionUtils


class UserView(APIView):
    """User register"""
    permission_classes = (AllowAny,)

    def post(self, request):

        # try creating the user, else return the appropriate exception
        try:
            message = UserManager.create_user_account(request)
            status_code = status.HTTP_201_CREATED
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            print(f'{error} sdadasdasddsa')
            return CustomExceptionUtils.user_custom_exception_handler(error)
    
    def get(self, request):
        try:
            message = UserManager.is_user_active(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response_data(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.user_custom_exception_handler(error)


class ResendActivationEmailView(APIView):
    """ Currently only the resend activation email functionality """
    permission_classes = (AllowAny,)

    def post(self, request):
        # try resending email, else return appropriate exception
        try:
            message = UserManager.resend_activation_email(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.user_custom_exception_handler(error)


class PasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            message = UserManager.password1(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.user_custom_exception_handler(error)



class UserLogin(KnoxLoginView):
    """User login"""
    permission_classes = (AllowAny,)
    
    def post(self, request):
        try:
            message = UserManager.login_user(request)
            status_code = status.HTTP_202_ACCEPTED
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.user_custom_exception_handler(error)
    

class UserProfile(APIView):
    """User S.E.D(search, edit, delete)"""

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    # def put(self, request):
    #     try:
    #         message = User.edit_profile(request)
    #         status_code = 200
    #         return handle_response(status_code, message)
    #     except Exception as e:
    #         return user_custom_exception_handler(e)

        
    def delete(self, request):
        try:
            message = UserManager.delete_user_account(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.user_custom_exception_handler(error)

        
    def get(self, request):

        # try getting the user, else return the appropriate exception
        try:
            message = UserManager.get_user_account(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response_data(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.user_custom_exception_handler(error)
    
# ________ RoomVIEWS ________ #

class RoomView(APIView):
    """Room Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            message = RoomManager.create_room(request)
            status_code = status.HTTP_201_CREATED
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.room_custom_exception_handler(error)

    def delete(self, request):
        try:
            message = RoomManager.delete_room(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.room_custom_exception_handler(error)

    def put(self, request):
        try:
            message = RoomManager.edit_room(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.room_custom_exception_handler(error)
    

class RoomExtendedView(APIView):
    """Room Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            message = RoomManager.join_room(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.room_custom_exception_handler(error)

    def delete(self, request):
        try:
            message = RoomManager.leave_room(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.room_custom_exception_handler(error)
        
    def get(self, request):
        try:
            message = RoomManager.get_user_participating_rooms(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response_data(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.room_custom_exception_handler(error)

# ________ StreamVIEWS ________ #

class StreamView(APIView):
    """Stream Controller"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            message = StreamManager.create_stream(request)
            status_code = status.HTTP_201_CREATED
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            CustomExceptionUtils.stream_custom_exception_handler(error)

    def put(self, request):
        try:
            message = StreamManager.edit_stream(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response(status_code, message)
        except Exception as error:
            CustomExceptionUtils.stream_custom_exception_handler(error)
    
    def get(self, request):
        try:
            message = StreamManager.display_history(request)
            status_code = status.HTTP_200_OK
            return HandleResponseUtils.handle_response_data(status_code, message)
        except Exception as error:
            return CustomExceptionUtils.room_custom_exception_handler(error)

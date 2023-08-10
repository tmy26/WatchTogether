from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .backend_logic import create_user, get_user
from .backend_logic_rooms import *
from .backend_logic_stream import create_stream, edit_stream


class UserRegistrationView(APIView):
    """User registration"""

    def post(self, request):
        msg = create_user(request)
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg, status=status.HTTP_200_OK)


class GetUserView(APIView):
    """Search for user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        msg = get_user(request)
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg.data, status=status.HTTP_200_OK)


class RoomCreationView(APIView):
    """Room creation"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return handle_response(create_room(request))

    def delete(self, request):
        return handle_response(delete_room(request))

    def put(self, request):
        return handle_response(edit_room(request))

    def get(self, request):
        msg = get_room()
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg.data, status=status.HTTP_200_OK)


class JoinRoomView(APIView):
    """Other users join/leave rooms"""

    def post(self, request):
        return handle_response(join_room(request))

    def delete(self, request):
        return handle_response(leave_room(request))

    def get(self, request):
        msg = list_rooms_user_participates(request)
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg.data, status=status.HTTP_200_OK)


class StreamCreationView(APIView):
    """Stream creation, deletion, and editing"""
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        return handle_response(create_stream(request))

    def put(self, request):
        return handle_response(edit_stream(request))


# ---------Support Functions--------- #

def handle_response(msg):
    if isinstance(msg, dict) and 'Error' in msg.keys():
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data=msg, status=status.HTTP_200_OK)

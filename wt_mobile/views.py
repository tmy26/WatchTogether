from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .backend_logic import  delete_user_account, create_user, get_user
from .backend_logic_rooms import *
from .backend_logic_stream import * 


class UserRegistrationView(APIView):
    """User registration"""

    def post(self, request):
        msg = create_user(request)
        if isinstance(msg,dict) and 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg, status=status.HTTP_200_OK)


class EditUserView(APIView):
    """R.U.D methods for user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        msg = get_user(request)
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg.data, status=status.HTTP_200_OK)

    def put(self):
        pass
    
    def delete(self, request):
        msg = delete_user_account(request)
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
        msg = get_room(request)
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

   
    def post(self, request):
        return handle_response(create_steam(request))

    def put(self, request):
        return handle_response(edit_stream(request))


# ---------Support Functions--------- #

def handle_response(msg):
    if isinstance(msg, dict) and 'Error' in msg.keys():
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data=msg, status=status.HTTP_200_OK)

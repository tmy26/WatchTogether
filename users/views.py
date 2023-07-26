from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .backend_logic import  delete_user_account, create_user, get_user
from .backend_logic_rooms import create_room
from .backend_logic_rooms import *
from .backend_logic_stream import * 


class UserRegistration(APIView):
    """User registration"""

    def post(self, request):
        msg = create_user(request)
        if isinstance(msg,dict) and 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg, status=status.HTTP_200_OK)


class EditUser(APIView):
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


class RoomCreation(APIView):
    """Room creation"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        msg = create_room(request)
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg, status=status.HTTP_200_OK)

    def delete(self, request):
        msg = delete_room(request)
        if 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg, status=status.HTTP_200_OK)
    
    def put(self, request):
        msg = edit_room(request)
        if 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg, status=status.HTTP_200_OK)

    def get(self, request):
        msg = get_room(request)
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg.data, status=status.HTTP_200_OK)
        
# TODO: Investigate on how to join a room using the GET method.
# TODO: Display rooms for currently logged user

class StreamCreation(APIView):
    """Stream creation, deletion, and editing"""

   
    def post(self, request):
        return handle_response(create_steam(request))

    def put(self, request):
        return handle_response(edit_stream(request))

    def get(self, request):
        return handle_response(get_stream(request).data)
    
def handle_response(msg):
    if isinstance(msg, dict) and 'Error' in msg.keys():
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data=msg, status=status.HTTP_200_OK)

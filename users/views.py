from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .backend_logic import create_user, delete_user_account, user_authentification
from .backend_logic_rooms import *
from .backend_logic_stream import * 


class UserRegistration(APIView):
    """User registration"""

    def post(self, request):
        msg = create_user(request)
        if 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'Success': 'Created user'}, status=status.HTTP_200_OK)
        
    def put(self, request):
        pass

    def delete(self, request):
        msg = delete_user_account(request)
        if 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg, status=status.HTTP_200_OK)


class UserAuthentification(APIView):
    """User auth"""

    def post(self, request):
        msg = user_authentification(request)
        return msg


class RoomCreation(APIView):
    """Room creation"""

    def post(self, request):
        msg = create_room(request)
        if 'Error' in msg.keys():
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
    

class StreamCreation(APIView):
    """Stream creation"""


    def post(self, request):
        msg, created_object = create_steam(request)
        return handle_response(msg), created_object

    def delete(self, request):
        msg, deleted_object = delete_stream(request)
        return handle_response(msg), deleted_object

    def put(self, request):
        msg, edited_object = edit_stream(request)
        return handle_response(msg), edited_object


def handle_response(msg):
    if isinstance(msg, dict) and 'Error' in msg.keys():
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data=msg, status=status.HTTP_200_OK)
    
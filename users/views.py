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
        return self.handle_response(create_steam(request), "Stream was created")

    def put(self, request):
        return self.handle_response(edit_stream(request), "Stream was edited")

    def get(self, request):
        return self.handle_response(get_stream(request))

def handle_response(self, msg, success_msg=None):
    if isinstance(msg, dict) and 'Error' in msg:
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
    else:
        if success_msg:
            return Response(data=msg, status=status.HTTP_200_OK)
        else:
            return Response(data=msg, status=status.HTTP_200_OK)
    
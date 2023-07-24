from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .backend_logic import create_user, delete_user_account, user_authentification
from .backend_logic_rooms import *


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
            return Response(data={'Success': 'Created room'}, status=status.HTTP_200_OK)


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
        

class JoinRoom(APIView):
    """Other users join/leave rooms"""

    def post(self, request):
        msg = join_room(request)
        if 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg, status=status.HTTP_200_OK)
    

    def delete(self, request):
        msg = leave_room(request)
        if 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg, status=status.HTTP_200_OK)
    

    def get(self, request):
        msg = list_rooms_user_participates(request)
        if isinstance(msg, dict) and 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=msg.data, status=status.HTTP_200_OK)
        
# TODO: Display all rooms for the user
# TODO: username's room [number] - idea for a filter field
# TODO: think of refactoring all request mapping

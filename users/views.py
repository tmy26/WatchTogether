from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .backend_logic import create_user
from .backend_logic_rooms import create_room

class UserRegistration(APIView):
    """User registration"""

    def post(self, request):
        msg = create_user(request)
        if 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'Success': 'Created user'}, status=status.HTTP_200_OK)


class RoomCreation(APIView):
    """Room creation"""

    def post(self, request):
        msg = create_room(request)
        if 'Error' in msg.keys():
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'Success': 'Created room'}, status=status.HTTP_200_OK)
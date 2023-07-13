from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .backend_logic import function

class UserRegistration(APIView):
    """C.R.U.D"""

    def get(self, request) -> Response:

        data = {'Message:': 'success'}
        return Response(data=data, status=status.HTTP_200_OK)
    

    def post(self, request):

        data = {'Message:': 'success'}
        return Response(data=data, status=status.HTTP_200_OK)
    

    def put(self, request):

        data = {'Message:': 'success'}
        return Response(data=data, status=status.HTTP_200_OK)
    

    def delete(self, request):

        data = {'Message:': 'success'}
        return Response(data=data, status=status.HTTP_200_OK)

# chat_app/views.py
from .chat_manager import ChatManager

from django.http import JsonResponse
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from wt_mobile.utils import CustomExceptionUtils


class MessageView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """ Returns all the previous messages for a room """
        try:
            result = ChatManager.get_previous_messages(request)
            status_code = status.HTTP_200_OK
            # Return messages as JSON response
            return JsonResponse(data=result, safe=False, status=status_code)
        except Exception as error:
            return CustomExceptionUtils.chat_custom_exception_handler(error)

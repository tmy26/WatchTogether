# chat_app/views.py
from .chat_manager import ChatManager
from .stream_manager import StreamManager

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


class StreamHistoryView(APIView):

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        """ Returns all the youtube links, previously played in this room  """

        try:
            result = StreamManager.get_stream_history(request)
            status_code = status.HTTP_200_OK

            # If the obj is type set return list(obj)

            if isinstance(result, set):
                return JsonResponse(data=list(result), status=status_code, safe=False)
            else:
                return JsonResponse(data=result, status=status_code, safe=False)
        except Exception as error:
            return CustomExceptionUtils.room_custom_exception_handler(error)

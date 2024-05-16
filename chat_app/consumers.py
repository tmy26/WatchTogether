# chat_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, StreamHistory
from channels.db import database_sync_to_async
from watch_together.general_utils import get_loggers
from .utils import get_room, get_user

DEV_LOGGER = get_loggers('dev_logger')


class ChatConsumer(AsyncWebsocketConsumer):
    """ Communicate with WebSocket """

    async def connect(self):
        """ Connecting to the WebSocket """

        self.user_obj = None
        headers = dict(self.scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    self.user_obj = await database_sync_to_async(get_user)(token_key=token_key)

            except Exception:
                # Ensures that the user will be authenticated before handshaking with WebSocket
                error_msg = "Authorizing the User raised an exception while trying to handshake with WebSocket.\
                                Refer to 'connect()' inside consumers.py"
                DEV_LOGGER.error(error_msg, exc_info=True)
                await self.close()
                return
        else:
            # Ensures that the user will be authenticated before handshaking with WebSocket
            error_msg = "Authorizing the User raised an exception while trying to handshake with WebSocket.\
                                Refer to 'connect()' inside consumers.py"
            DEV_LOGGER.error(error_msg, exc_info=True)
            await self.close()
        
        if self.user_obj is None:
            # Ensures that the user will be authenticated before handshaking with WebSocket
            error_msg = "Authorizing the User raised an exception while trying to handshake with WebSocket.\
                                Refer to 'connect()' inside consumers.py"
            DEV_LOGGER.error(error_msg, exc_info=True)
            await self.close()

        self.unique_id = self.scope['url_route']['kwargs']['unique_id']
        self.room_group_name = f'chat_{self.unique_id}'

        # Check if the room exists in the database and get room object
        try:
            self.room_obj = await database_sync_to_async(get_room)(unique_id=self.unique_id)
        except Exception:
            # Ensures that room exists before handshaking with WebSocket
            error_msg = "Getting the Room object raised an exception while trying to handshake with WebSocket.\
                                Refer to 'connect()' inside consumers.py"
            DEV_LOGGER.error(error_msg, exc_info=True)
            await self.close()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """ Disconnect from the WebSocket """

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        receive_type = text_data_json['type'] # can be video or chat_message

        # do action depending on what is the receive type
        if receive_type == "chat_message":

            message = text_data_json['message']
            username = text_data_json['username']

            # Save message to database
            await self.save_messages(text_data_json["message"])

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': receive_type,
                    'message': message,
                    'username': username
                }
            )

        elif receive_type == "video":
            video_url = text_data_json['video_url']

            # Save to stream history
            await self.add_video_play_history(video_url)

            # Broadcast video URL to all clients in room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': receive_type,
                    'video_url': video_url
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        send_type = event['type']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'type': send_type
        }))
    
    async def video(self, event):
        video_url = event['video_url']
        send_type = event['type']

        # Send video back to WebSocket
        await self.send(text_data=json.dumps({
            'video_url': video_url,
            'type': send_type
        }))

    @sync_to_async
    def save_messages(self, message):
        """ Save message to database """

        Message.objects.create(
            room=self.room_obj,
            sender=self.user_obj,
            content=message
        )
    
    @sync_to_async
    def add_video_play_history(self, video):
        """ Saves to stream history db """

        StreamHistory.objects.create(
            room=self.room_obj,
            link=video
        )

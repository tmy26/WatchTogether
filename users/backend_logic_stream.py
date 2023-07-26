from .models import Room , Stream
from users.serializers import StreamSerializer
from django.core.exceptions import MultipleObjectsReturned


def create_steam(request) -> dict:
    """Stream creation function"""

    try:
        # request data
        link = request.data.get('link')
        assigned_room = request.data.get('assigned_room')

        # Check if assigned_room is provided and if the room exists
        if not assigned_room or not Room.objects.filter(room_unique_id=assigned_room).exists():
            return {"Error": "Invalid 'assigned_room'. The room does not exist."}

        room = Room.objects.get(room_unique_id=assigned_room)

        # Check if the room already has a stream assigned
        if Stream.objects.filter(assigned_room=room).exists():
            return {"Error": "The room already has a stream assigned."}
        else:
            Stream.objects.create(link=link, assigned_room=room)
            return {'Success': 'Stream created'}

    except Exception as e:
        return {"Error": "An error occurred. Please check the provided data and try again."}
    
        

def edit_stream(request) -> dict:
        """Stream editing function"""
        link = request.data.get('link')
        assigned_room = request.data.get('assigned_room')

        # Check if assigned_room is provided and if the room exists
        if not assigned_room or not Room.objects.filter(room_unique_id=assigned_room).exists():
            return {"Error": "Invalid 'assigned_room'. The room does not exist."}

        # Check if requested data is null
        if not link:
            return {"Error": "Invalid data. 'link' is required."}

        try:
            stream_to_edit = Stream.objects.get(assigned_room=assigned_room)
            stream_to_edit.link = link
            stream_to_edit.save()
            return {'Success': 'Stream edited'}
        except (Stream.DoesNotExist, Room.DoesNotExist, MultipleObjectsReturned):
            return {"Error": "Stream or Room does not exist or multiple objects returned."}
        

def get_stream(request) -> dict:
    """Get stream function"""
    try:
        all_stream_objs = Stream.objects.all()
        serialized = StreamSerializer(all_stream_objs, many=True)
        return serialized.data  # Return the serialized data instead of the entire serializer object

    except Stream.DoesNotExist:
        return {"Error": "Stream does not exist!"}
    
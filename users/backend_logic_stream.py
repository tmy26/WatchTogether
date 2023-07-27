from .models import Room , Stream
from users.serializers import StreamSerializer
from django.core.exceptions import MultipleObjectsReturned ,ValidationError


def create_steam(request) -> dict:
    """Stream creation function"""

        # request data
    link = request.data.get('link')
    assigned_room = request.data.get('assigned_room')
    try:
        # Check if assigned_room is provided and if the room exists
        if not assigned_room:
            return {"Error": "Assigned room is required."}  
        # Check if assigned_room is provided and if the room exists
        if assigned_room and Room.objects.filter(room_unique_id=assigned_room).exists():
            room = Room.objects.get(room_unique_id=assigned_room)

        # Check if the room already has a stream assigned
            if Stream.objects.filter(assigned_room=room).exists():
                return {"Error": "The room already has a stream assigned."}
            else:
                Stream.objects.create(link=link, assigned_room=room)
                return {'Success': 'Stream created'}
    except (Stream.DoesNotExist, Room.DoesNotExist, MultipleObjectsReturned, ValidationError):
            return {"Error": "Something went wrong with the data you provided please check if the data is correct and try again."}
    

def edit_stream(request) -> dict:
    """Stream editing function"""
    link = request.data.get('link')
    assigned_room = request.data.get('assigned_room')

    
    try:
        # Check if requested data is null
        if not link or not assigned_room:
            return {"Error": "Invalid data. 'link' and/or 'assigned_room' is required."}
        # Check if assigned_room is provided and if the room exists
        if assigned_room and Room.objects.filter(room_unique_id=assigned_room).exists():

            stream_to_edit = Stream.objects.get(assigned_room=assigned_room)
            stream_to_edit.link = link
            stream_to_edit.save()
    except (Stream.DoesNotExist, Room.DoesNotExist, MultipleObjectsReturned, ValidationError):
        return {"Error": "Something went wrong with the data you provided please check if the data is correct and try again."}
        
    return {'Success': 'Stream edited'}    
        
        
def get_stream() -> dict:
    """Get stream function"""
    try:
        all_stream_objs = Stream.objects.all()
        serialized = StreamSerializer(all_stream_objs, many=True)
    except (Stream.DoesNotExist, MultipleObjectsReturned):
        return {"Error": "Stream does not exist or mulpiple objects returned."}
    
    return serialized  

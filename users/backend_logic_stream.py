from .models import Room , Stream


def create_steam(request) -> dict:
    """Stream creation function"""

    # request data
    stream_link = request.data.get('stream_link' )
    stream_room = request.data.get('stream_room')

     # Check if stream_room is provided and if the room exists
    if not stream_room or not Room.objects.filter(room_unique_id=stream_room).exists():
        return {"Error": "Invalid 'stream_room'. The room does not exist."}

    #check if requested data is null
    if not stream_link:
        return {"Error": "Invalid data. 'stream_link' is required."}

    room = Room.objects.get(room_unique_id=stream_room)

     # Check if the room already has a stream assigned
    if Stream.objects.filter(stream_room=room).exists():
        return {"Error": "The room already has a stream assigned."}
    Stream.objects.create(
    stream_link = stream_link,
    stream_room=room
    )
    return {'Success': 'Stream created'}
        

def delete_stream(request) -> dict:
    """Stream deletion function"""
    stream_room = request.data.get('stream_room')

    # Check if stream_room is provided and if the room exists
    if not stream_room or not Room.objects.filter(room_unique_id=stream_room).exists():
        return {"Error": "Invalid 'stream_room'. The room does not exist."}

    try:
        stream_to_delete = Stream.objects.get(stream_room=stream_room)
        stream_to_delete.delete()
        return {'Success': 'Stream deleted'}
    except Stream.DoesNotExist:
        return {"Error": "Stream does not exist"}


def edit_stream(request) -> dict:
        """Stream editing function"""
        stream_link = request.data.get('stream_link')
        stream_room = request.data.get('stream_room')

        # Check if stream_room is provided and if the room exists
        if not stream_room or not Room.objects.filter(room_unique_id=stream_room).exists():
            return {"Error": "Invalid 'stream_room'. The room does not exist."}

        # Check if requested data is null
        if not stream_link:
            return {"Error": "Invalid data. 'stream_link' is required."}

        try:
            stream_to_edit = Stream.objects.get(stream_room=stream_room)
            stream_to_edit.stream_link = stream_link
            stream_to_edit.save()
            return {'Success': 'Stream edited'}
        except Stream.DoesNotExist:
            return {"Error": "Stream does not exist"}
        except Room.DoesNotExist:
            return {"Error": "Room does not exist"}


def get_stream(request):
    """Get all streams from the database"""
    streams = Stream.objects.all()
    stream_data = []

    for stream in streams:
        stream_data.append({
            "stream_link": stream.stream_link,
            "stream_room": stream.stream_room.room_unique_id,
        })

    return stream_data

from .models import Room , Stream

def create_steam(request) -> dict:
    """Stream creation function"""

    # request data
    stream_link = request.data.get('stream_link')
    stream_room = request.data.get('stream_room')

    # Check if the sream_room is the same as the Id of the room and if it is creates the stream 

    try:
        room_unique_id = request.data.get('room_unique_id')

        if Stream.objects.filter(stream_room=room_unique_id).exists(): 
         Stream.objects.create(
        stream_link = stream_link,
        stream_room=stream_room
        )
        Stream.save()
        return {'Success': 'Stream created'}
    except Room.DoesNotExist:
        return {"Error": 'Create a room First and then create the stream'}
    

def delete_stream(request) -> dict:
    """Delete stream function"""

    # Get the room that the stream belongs
    stream_room = request.data.get('stream_room')
    room_unique_id = request.data.get('room_unique_id')

    try:
        Stream.objects.get(stream_room=room_unique_id).delete()
        return {"Success": "Stream deleted"}
    except Stream.DoesNotExist:
        return {"Error": "Stream does not exist"}


def edit_stream(request) -> dict:
    """Edit stream function"""

    # Get the id ot the room and stream properties 
    room_unique_id = request.data.get('room_unique_id')
    new_stream_link = request.data.get('stream_link')
    new_stream_room = request.data.get('stream_room')
    stream_room = request.data.get('stream_room')


    try:
        if Stream.objects.filter(stream_room=room_unique_id).exists():
            stream_to_edit = Stream.objects.get(stream_room=stream_room)
            if new_stream_link:
                stream_to_edit.stream_link = new_stream_link
            stream_to_edit.save()
        return {"Success": "Stream edited"}
    except Stream.DoesNotExist:
        return {"Error": "Stream does not exist"}

from .models import Room , Stream
from django.core.exceptions import MultipleObjectsReturned ,ValidationError


def create_steam(request) -> dict:
    """Stream creation function"""

        # request data
    link = request.data.get('link')
    assigned_room = request.data.get('assigned_room')

     #Check if assigned_room is provided and if the room exists
    if not assigned_room:
        return {"Error": "Assigned room is required."}  
    try:
        #Check if the room exists
        room = Room.objects.get(room_unique_id=assigned_room)
    
        # Check if the room already has a stream assigned
        if Stream.objects.filter(assigned_room=room).exists():
            return {"Error": "The room already has a stream assigned."}
        
        created_stream = Stream(link=link, assigned_room=room)
        created_stream.save() 
    except (Stream.DoesNotExist, Room.DoesNotExist, MultipleObjectsReturned, ValidationError):
        return {"Error": "Something went wrong with the data you provided please check if the data is correct and try again."}
    
    return {'Success': 'Stream created'}
    
    

def edit_stream(request) -> dict:
    """Stream editing function"""
    link = request.data.get('link')
    assigned_room = request.data.get('assigned_room')

    # Check if requested data is null
    if not link or not assigned_room:
        return {"Error": "Invalid data. 'link' and/or 'assigned_room' is required."}
    try:
        # Check if assigned_room is provided and if the room exists
        if assigned_room and Room.objects.filter(room_unique_id=assigned_room).exists():

            stream_to_edit = Stream.objects.get(assigned_room=assigned_room)
            stream_to_edit.link = link
            stream_to_edit.save()
    except (Stream.DoesNotExist, Room.DoesNotExist, MultipleObjectsReturned, ValidationError):
        return {"Error": "Something went wrong with the data you provided please check if the data is correct and try again."}
        
    return {'Success': 'Stream edited'}    
        
    #TODO link verification
from .models import Room, Stream
from django.core.exceptions import MultipleObjectsReturned, ValidationError
import requests

# dev_loggers = get_loggers('wt_mobile_dev')
ERROR = 'Error'
SUCCESS = 'Success'
ERROR_MESSAGE = {'Error': 'Something went wrong with the data you provided. Please check if the data is correct and try again.'}


def create_stream(request):
    """Stream creation function"""

    try:
        # Extract data from the request
        link = request.data.get('link')
        assigned_room = request.data.get('assigned_room')

        # Check if assigned_room is provided
        if not assigned_room:
            return {ERROR: 'Assigned room is required.'}

        # Check if the room exists
        room = Room.objects.get(unique_id=assigned_room)

        # Check if the room already has a stream assigned
        if Stream.objects.filter(assigned_room=room).exists():
            return {ERROR: 'The room already has a stream assigned.'}

        # Validate the provided link using the validate_link function
        link_validation_result = validate_link(link)
        if link_validation_result:
            return link_validation_result

        # Create and save a new Stream instance
        created_stream = Stream(link=link, assigned_room=room)
        created_stream.save()

    except Room.DoesNotExist:
        return {ERROR: 'Assigned room does not exist.'}
    except (Stream.DoesNotExist, MultipleObjectsReturned, ValidationError, requests.exceptions.InvalidURL):
        return ERROR_MESSAGE

    # Return a success message
    return {SUCCESS: 'Stream created'}
    
def edit_stream(request) -> dict:
    """Stream editing function"""

    # Extract data from the request
    link = request.data.get('link')
    assigned_room = request.data.get('assigned_room')

    # Check if requested data is null
    if not link or not assigned_room:
        return ERROR_MESSAGE
    try:
        # Check if assigned_room is provided and if the room exists
        if assigned_room and Room.objects.filter(unique_id=assigned_room).exists():

            # Validate the provided link using the validate_link function
            link_validation_result = validate_link(link)
            if link_validation_result:
                return link_validation_result
            
            # Retrieve the stream to edit
            stream_to_edit = Stream.objects.get(assigned_room=assigned_room)
            
            # Update the stream link and save the changes
            stream_to_edit.link = link
            stream_to_edit.save()

    except (Stream.DoesNotExist, Room.DoesNotExist, MultipleObjectsReturned, ValidationError, requests.exceptions.InvalidURL):
        return ERROR_MESSAGE
        
    return {SUCCESS: 'Stream edited'}


# ---------Support Functions--------- #

def validate_link(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            #if the method is able to open the website it returns none
            return None
        else:
            return {ERROR: 'Link is valid, but the website returned a non-OK status code.'}
    except requests.exceptions.RequestException:
        return {ERROR: 'Link is not valid or could not be accessed.'}

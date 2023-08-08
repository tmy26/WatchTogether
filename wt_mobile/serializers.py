from rest_framework import  serializers
from .models import User, Stream, UserRoom


class UserSerializer(serializers.ModelSerializer):
    """User serializer, returns all fields that the user has"""
    class Meta:
        model = User
        fields = '__all__'


class UserSerializerSearchByUsername(serializers.ModelSerializer):
    """User serializer used to return username only"""
    class Meta:
        model = User
        fields = ['username']


class JoinedRoomSerializer(serializers.ModelSerializer):
    """Serializer for displaying the following fields of the joined UserRoom table"""

    class Meta():
        model = UserRoom
        fields = ['room_name', 'date_joined']


class StreamSerializer(serializers.ModelSerializer):
    """Stream serializer used to return all created streams"""

    class Meta():
        model = Stream
        fields = '__all__'
        
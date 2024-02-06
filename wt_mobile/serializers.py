from rest_framework import serializers
from .models import Stream, StreamHistory, User, Room


class UserSerializerSearchByUsername(serializers.ModelSerializer):
    """User serializer used to return username only"""
    class Meta:
        model = User
        fields = ['last_login', 'date_joined', 'username', 'email']


class UserSerializerCheckIfUserActive(serializers.ModelSerializer):
    """Returns the is_active field"""
    class Meta():
        model = User
        fields = ['is_active']
        

class JoinedRoomSerializer(serializers.ModelSerializer):
    """Serializer for displaying the following fields of the joined UserRoom table"""
    class Meta():
        model = Room
        fields = ['unique_id', 'name', 'owner_id']


class StreamSerializer(serializers.ModelSerializer):
    """Stream serializer used to return all created streams"""
    class Meta():
        model = Stream
        fields = '__all__'


class StreamHistorySerializer(serializers.ModelSerializer):
    """Display the history for the current stream"""
    class Meta():
        model = StreamHistory
        fields = ('link', 'time_when_played')

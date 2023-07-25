from rest_framework import  serializers
from .models import Room , Stream

class RoomSerializer(serializers.ModelSerializer):

    class Meta():
        model = Room
        fields = '__all__'


class StreamSerializer(serializers.ModelSerializer):


    class Meta():
        model = Stream
        fields = '__all__'
        
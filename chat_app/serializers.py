from rest_framework import serializers
from .models import StreamHistory

class StreamHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StreamHistory

        fields = ["room_id", "link"]

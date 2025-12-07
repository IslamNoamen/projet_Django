from rest_framework import serializers

from SessionApp.models import Session


class SessionSerializer(serializers.ModelSerializer):
    """
    Serialize / deserialize `Session` instances for the API.
    """

    class Meta:
        model = Session
        fields = [
            'session_id',
            'title',
            'topic',
            'room',
            'session_day',
            'start_time',
            'end_time',
            'conference',
            'created_at',
            'updated_at',
        ]


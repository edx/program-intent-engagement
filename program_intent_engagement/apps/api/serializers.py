"""
Serializers for the program-intent-engagement API
"""
from rest_framework import serializers

from program_intent_engagement.apps.core.models import ProgramIntent


class ProgramIntentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Program Intent Model
    """

    class Meta:
        """
        Meta Class
        """

        model = ProgramIntent
        fields = "__all__"

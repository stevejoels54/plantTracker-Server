from rest_framework import serializers
from .models import Reading, Notification


class ReadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reading
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'

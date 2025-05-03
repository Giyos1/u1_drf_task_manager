from rest_framework import serializers
from .models import Notification


class NotificationBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'to_user',
            'title',
            'descriptions',
            'is_read',
        ]


class NotificationListSerializer(NotificationBaseSerializer):
    class Meta(NotificationBaseSerializer.Meta):
        extra_kwargs = {
            'descriptions': {'read_only': True}
        }


class NotificationDetailSerializer(NotificationBaseSerializer):
    class Meta(NotificationBaseSerializer.Meta):
        extra_kwargs = {
            'is_read': {'write_only': True}
        }

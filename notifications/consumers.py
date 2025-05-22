import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user']:
            await self.close()
        await self.channel_layer.group_add(f"notifications-{self.scope['user']}", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(f"notifications-{self.scope['user']}", self.channel_name)

    async def receive(self, text_data):
        # Buni odatda frontenddan yuborilgan so‘rovlar uchun ishlatiladi
        await self.channel_layer.group_send(
            f"notifications-{self.scope['user']}",
            {
                "type": "send_notification",
                "message": text_data
            }
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))


class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("test", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("test", self.channel_name)

    async def receive(self, text_data):
        # Buni odatda frontenddan yuborilgan so‘rovlar uchun ishlatiladi
        await self.channel_layer.group_send(
            "test",
            {
                "type": "send_notification",
                "message": text_data
            }
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))


def notify_user(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_notification",
            "message": message,
        }
    )

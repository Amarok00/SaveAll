import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    """Async websocket consumer to process notifications"""

    async def connect(self):
        """Connect to notification group"""
        print("connected")
        self.user = self.scope["user"]
        self.room_name = self.user.username
        self.room_group_name = f"notifications_{self.room_name}"
        if self.user.is_authenticated:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Disconnect from notification group"""
        print("disconnected")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_notification(self, event):
        """Send notification to WebSocket"""
        await self.send(text_data=json.dumps(event))

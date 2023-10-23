
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Message, CustomUser,ChatRoom

# class PersonalChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         my_id = self.scope['user'].id
#         other_user_id = self.scope['url_route']['kwargs']['id']
#         if int(my_id) > int(other_user_id):
#             self.room_name = f'{my_id}-{other_user_id}'
#         else:
#             self.room_name = f'{other_user_id}-{my_id}'

#         self.room_group_name = 'chat_%s' % self.room_name

#         await self.channel_layer.group_add.delay(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def receive(self, text_data=None, bytes_data=None):
#         data = json.loads(text_data)
#         print(data)
#         message = data['message']
#         username = data['username']
#         receiver = data['receiver']

#         await self.save_message(username, self.room_group_name, message, receiver)

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'username': username,
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']
#         print(message)
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username
#         }))

#     async def disconnect(self, code):
#         self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        receiver = data['receiver']

        await self.save_message(username, self.room_group_name, message, receiver)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, sender_username, room_name, message_content, receiver_username):
        sender = CustomUser.objects.get(username=sender_username)
        receiver = CustomUser.objects.get(username=receiver_username)
        room = ChatRoom.objects.get(name=room_name)

        message = Message.objects.create(
            room=room,
            content=message_content,
            sender=sender,
            recipient=receiver
        )
        return message

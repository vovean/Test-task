import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class TaskConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # Add ourselves to the group so we can get notified when different events happen
        async_to_sync(self.channel_layer.group_add)(
            'tasks_group',
            self.channel_name
        )

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        # Actually we are not supposed to get messages from the client
        # Still just in case we somewhy do receive one print it
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

    def tasks_group_message(self, event):
        # Receive group message (from change_status view) and send it to client
        message = event['message']
        self.send(text_data=message)

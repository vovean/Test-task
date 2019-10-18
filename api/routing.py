from django.urls import path

import api.consumers as consumers

websocket_urlpatterns = [
    path(r'ws/tasks/', consumers.TaskConsumer),
]

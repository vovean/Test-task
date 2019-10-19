import json

from asgiref.sync import async_to_sync

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from api.models import Task
from api.serializers import TaskSerializer

import channels.layers


class TaskList(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner_id', 'finished']


# Добавление задачи
class CreateTask(CreateAPIView):
    serializer_class = TaskSerializer


@csrf_exempt
def change_task_status(request, task_id):
    if not request.method == 'GET':
        return JsonResponse(data={'detail': 'Method "POST" not allowed.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        task_to_finish = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse(data={'detail': 'Not found.'},
                            status=status.HTTP_404_NOT_FOUND)
    task_to_finish.change_status()

    # Channels notifications to everyone who is in 'tasks_group' group
    channel_layer = channels.layers.get_channel_layer()
    message = {
        'task_id': task_id,
        'action': 'change_status'
    }
    async_to_sync(channel_layer.group_send)('tasks_group', {
        'type': 'tasks_group_message',
        'message': json.dumps(message)
    })
    return JsonResponse(data=TaskSerializer(task_to_finish).data,
                        status=status.HTTP_200_OK)


# Удаление задачи
class DeleteTask(DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'

import time

from django.http import JsonResponse

from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from api.models import Task
from api.serializers import TaskSerializer
from api.status_updater import StatusUpdater

import settings.settings as settings


class TaskList(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner_id', 'finished']


# Добавление задачи
class CreateTask(CreateAPIView):
    serializer_class = TaskSerializer


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

    StatusUpdater.get_status_update(task_id, task_to_finish.finished)

    return JsonResponse(data=TaskSerializer(task_to_finish).data,
                        status=status.HTTP_200_OK)


# Удаление задачи
class DeleteTask(DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'


# long polling
def listen_to_updates(request):
    while not StatusUpdater.has_updates:
        # keeping connection open
        time.sleep(settings.UPDATE_FREQUENCY)
    return StatusUpdater.get_response()

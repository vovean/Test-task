from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from api.models import Task
from api.serializers import TaskSerializer
from api.ajax_updater import AjaxUpdater

can_return_ajax = False
ajax_response = None


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

    AjaxUpdater.get_status_update(task_id)

    return JsonResponse(data=TaskSerializer(task_to_finish).data,
                        status=status.HTTP_200_OK)


# Удаление задачи
class DeleteTask(DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'


# long polling
def listen_to_updates(request):
    while not AjaxUpdater.has_updates:
        # keeping connection open
        ...
    return AjaxUpdater.get_response()

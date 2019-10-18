from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from api.models import Task
from api.serializers import TaskSerializer


# TODO 5. Метод ожидания перевода задачи в статус "Выполнена" по уникальному идентификатору с помощью long pooling


# TODO 4. Метод получения списка задач с указанием фильтра по статусу задачи
class TaskList(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner_id', 'finished']


# TODO 1. Метод добавления задачи
class CreateTask(CreateAPIView):
    serializer_class = TaskSerializer


# TODO 2. Метод изменения статуса задачи
@csrf_exempt
def change_task_status(request, task_id):
    task_to_finish = Task.objects.get(id=task_id)
    task_to_finish.change_status()
    # TODO Channels notofications
    return JsonResponse(data=TaskSerializer(task_to_finish).data, status=status.HTTP_200_OK)


# TODO 3. Метод удаления задачи
class DeleteTask(DestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_url_kwarg = 'task_id'

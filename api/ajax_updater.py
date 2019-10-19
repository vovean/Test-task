from django.http import JsonResponse
from rest_framework import status


class AjaxUpdater:
    has_updates = False
    __response = None

    @classmethod
    def get_status_update(cls, task_id):
        AjaxUpdater.__response = JsonResponse(data={'event': 'change_status', 'task_id': task_id},
                                              status=status.HTTP_200_OK)
        AjaxUpdater.has_updates = True

    @classmethod
    def get_response(cls):
        AjaxUpdater.has_updates = False
        return AjaxUpdater.__response

import json

from django.http import JsonResponse
from rest_framework import status


class StatusUpdater:
    has_updates = False
    __response = dict()

    @classmethod
    def get_status_update(cls, task_id, new_status):
        # For each task_id we store only last update on its status
        StatusUpdater.__response[task_id] = new_status
        StatusUpdater.has_updates = True

    @classmethod
    def get_response(cls):
        StatusUpdater.has_updates = False
        json_response = JsonResponse({'event': 'status_updates', 'data': StatusUpdater.__response})
        StatusUpdater.__response = dict()
        return json_response

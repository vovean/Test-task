from django.urls import path
import api.views as views

import settings.settings as settings

urlpatterns = [
    path('task/create', views.CreateTask.as_view()),
    path('task/<int:task_id>/change_status', views.change_task_status),
    path('task/<int:task_id>/delete', views.DeleteTask.as_view()),
    path('tasks/', views.TaskList.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('tasks/', views.TaskList.as_view())
    ]

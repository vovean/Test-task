from django.urls import path
import api.views as views

urlpatterns = [
    path('task/create', views.CreateTask.as_view()),
    path('task/<int:task_id>/change_status', views.change_task_status),
    path('task/<int:task_id>/delete', views.DeleteTask.as_view()),
    path('tasks/', views.TaskList.as_view()),
    path('listen_to_updates', views.listen_to_updates)
]

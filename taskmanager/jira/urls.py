from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="home"), 
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path("create_task", views.create_task, name="create_task"),
    path("create_sprint", views.create_sprint, name="create_sprint"),
    path("create_project", views.create_project, name="create_project"),
    path("list_tasks", views.TaskList.as_view(), name="task_list")
]

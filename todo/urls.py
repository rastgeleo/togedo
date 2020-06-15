from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TaskList.as_view(), name='task_list'),
    path(
        'completed/',
        views.TaskCompletedList.as_view(),
        name='task_completed_list'),
    path('create/', views.TaskCreate.as_view(), name='task_create'),
    path('<slug:slug>/', views.TaskDetail.as_view(), name='task_detail'),
    path(
        '<slug:slug>/update/',
        views.TaskUpdate.as_view(),
        name='task_update'
        ),
    path('<slug:slug>/delete/', views.TaskDelete.as_view(), name='task_delete')
]

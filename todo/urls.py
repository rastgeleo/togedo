from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    # path for tasklist
    path('', views.TaskListList.as_view(), name='tasklist_list'),
    path('create/', views.TaskListCreate.as_view(), name='tasklist_create'),
    path('<slug:slug>', views.TaskListDetail.as_view(),
         name='tasklist_detail'),

    # path for individual task
    path('<slug:list_slug>/create/', views.TaskCreate.as_view(),
         name='task_create'),
    path('<slug:list_slug>/<slug:task_slug>/', views.TaskDetail.as_view(),
         name='task_detail'),
    # path(
    #     'completed/',
    #     views.TaskCompletedList.as_view(),
    #     name='task_completed_list'),
    # path(
    #     'overdue/',
    #     views.TaskOverdueList.as_view(),
    #     name='task_overdue_list'
    # ),
    # path('create/', views.TaskCreate.as_view(), name='task_create'),
    # path(
    #     '<slug:slug>/update/',
    #     views.TaskUpdate.as_view(),
    #     name='task_update'
    #     ),
    # path('<slug:slug>/delete/', views.TaskDelete.as_view(), name='task_delete')
]

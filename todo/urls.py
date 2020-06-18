from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    # path for tasklist
    path('', views.TaskListList.as_view(), name='tasklist_list'),
    path('create/', views.TaskListCreate.as_view(), name='tasklist_create'),
    path('<slug:slug>/', views.TaskListDetail.as_view(),
         name='tasklist_detail'),
    path('<slug:slug>/update/', views.TaskListUpdate.as_view(),
         name='tasklist_update'),
    path('<slug:slug>/delete/', views.TaskListDelete.as_view(),
         name='tasklist_delete'),

    # path for individual task
    path('<slug:list_slug>/create/', views.TaskCreate.as_view(),
         name='task_create'),
    path('<slug:list_slug>/<slug:task_slug>/', views.TaskDetail.as_view(),
         name='task_detail'
         ),
    path(
        '<slug:list_slug>/<slug:task_slug>/update/',
        views.TaskUpdate.as_view(),
        name='task_update'
        ),
    path(
        '<slug:list_slug>/<slug:task_slug>/delete/',
        views.TaskDelete.as_view(),
        name='task_delete'
        ),
]

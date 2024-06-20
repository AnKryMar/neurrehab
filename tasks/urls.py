# tasks/urls.py
from django.urls import path
from . import views
from .views import TaskListView, TaskDetailView, ProfileStatisticsView, auto_task, image_match_auto

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('<str:category>/<str:task_type>/', TaskDetailView.as_view(), name='task_detail'),
    path('statistics/', ProfileStatisticsView.as_view(), name='profile_statistics'),
    path('auto/', auto_task, name='auto_task'),
    path('fruits/image_match/auto/', image_match_auto, name='image_match_auto'),
    path('admin/get_words_without_images/', views.get_words_without_images, name='get_words_without_images'),
    path('<task_type>/none/', TaskDetailView.as_view(), name='task_detail_no_category'),  # Для action_description без категории
]
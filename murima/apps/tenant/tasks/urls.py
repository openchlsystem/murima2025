# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Tasks
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<uuid:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    
    # Tags
    path('tags/', views.TaskTagListView.as_view(), name='tag-list'),
    path('tags/<uuid:pk>/', views.TaskTagDetailView.as_view(), name='tag-detail'),
    
    # Task Comments
    path('tasks/<uuid:task_id>/comments/', views.TaskCommentListView.as_view(), name='task-comment-list'),
    path('comments/<uuid:pk>/', views.TaskCommentDetailView.as_view(), name='task-comment-detail'),
    
    # Task Attachments
    path('tasks/<uuid:task_id>/attachments/', views.TaskAttachmentListView.as_view(), name='task-attachment-list'),
    path('attachments/<uuid:pk>/', views.TaskAttachmentDetailView.as_view(), name='task-attachment-detail'),
    
    # Task Reminders
    path('tasks/<uuid:task_id>/reminders/', views.TaskReminderListView.as_view(), name='task-reminder-list'),
    path('reminders/<uuid:pk>/', views.TaskReminderDetailView.as_view(), name='task-reminder-detail'),
    
    # Dashboard
    path('tasks/dashboard/', views.TaskDashboardView.as_view(), name='task-dashboard'),
    path('tasks/stats/', views.TaskCompletionStatsView.as_view(), name='task-stats'),
]
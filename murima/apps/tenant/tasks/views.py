from datetime import timedelta
from time import timezone
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import (
    Task, TaskTag, TaskTagging, TaskComment,
    TaskAttachment, TaskReminder
)
from .serializers import (
    TaskSerializer, TaskListSerializer, TaskTagSerializer,
    TaskCommentSerializer, TaskAttachmentSerializer,
    TaskReminderSerializer, TaskDashboardSerializer,
    TaskCompletionStatsSerializer
)
from cases.models import Case  # Assuming you have this
from users.permissions import IsSameTenant  # Custom permission you should implement

class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'status': ['exact', 'in'],
            'priority': ['exact', 'in', 'gte', 'lte'],
            'due_date': ['exact', 'gte', 'lte', 'isnull'],
            'created_at': ['exact', 'gte', 'lte'],
            'completed_at': ['exact', 'gte', 'lte', 'isnull'],
            'assigned_to': ['exact'],
            'created_by': ['exact'],
            'case': ['exact'],
            'workflow': ['exact'],
            'tags': ['exact'],
        }

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at', 'updated_at']
    ordering = ['-priority', 'due_date']

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.all()

        # Filter by tenant (using your tenant system)
        queryset = queryset.filter(tenant=user.tenant)

        # Apply additional filters from query params
        if self.request.query_params.get('overdue') == 'true':
            queryset = queryset.filter(
                due_date__lt=timezone.now(),
                status__in=[Task.Status.PENDING, Task.Status.IN_PROGRESS]
            )

        if self.request.query_params.get('mine') == 'true':
            queryset = queryset.filter(assigned_to=user)

        if self.request.query_params.get('q'):
            query = self.request.query_params.get('q')
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(comments__content__icontains=query)
            ).distinct()

        return queryset.select_related(
            'assigned_to', 'created_by', 'case'
        ).prefetch_related(
            'tags', 'subtasks'
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, tenant=self.request.user.tenant)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]
    lookup_field = 'pk'

    def get_queryset(self):
        return Task.objects.filter(
            tenant=self.request.user.tenant
        ).select_related(
            'assigned_to', 'created_by', 'case', 'workflow', 'parent_task'
        ).prefetch_related(
            'tags', 'subtasks', 'comments', 'attachments', 'reminders', 'change_logs'
        )

    def perform_update(self, serializer):
        serializer.save(_changed_by=self.request.user)

class TaskTagListView(generics.ListCreateAPIView):
    queryset = TaskTag.objects.all()
    serializer_class = TaskTagSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return super().get_queryset().filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class TaskTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskTagSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]
    lookup_field = 'pk'

    def get_queryset(self):
        return TaskTag.objects.filter(tenant=self.request.user.tenant)

class TaskCommentListView(generics.ListCreateAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        return TaskComment.objects.filter(
            task_id=task_id,
            task__tenant=self.request.user.tenant
        ).select_related('author')

    def perform_create(self, serializer):
        task = generics.get_object_or_404(
            Task.objects.filter(tenant=self.request.user.tenant),
            pk=self.kwargs.get('task_id')
        )
        serializer.save(task=task)

class TaskCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]
    lookup_field = 'pk'

    def get_queryset(self):
        return TaskComment.objects.filter(
            task__tenant=self.request.user.tenant
        ).select_related('author')

class TaskAttachmentListView(generics.ListCreateAPIView):
    serializer_class = TaskAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        return TaskAttachment.objects.filter(
            task_id=task_id,
            task__tenant=self.request.user.tenant
        ).select_related('uploaded_by')

    def perform_create(self, serializer):
        task = generics.get_object_or_404(
            Task.objects.filter(tenant=self.request.user.tenant),
            pk=self.kwargs.get('task_id')
        )
        serializer.save(task=task, uploaded_by=self.request.user)

class TaskAttachmentDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = TaskAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]
    lookup_field = 'pk'

    def get_queryset(self):
        return TaskAttachment.objects.filter(
            task__tenant=self.request.user.tenant
        ).select_related('uploaded_by')

class TaskReminderListView(generics.ListCreateAPIView):
    serializer_class = TaskReminderSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['remind_at']
    ordering = ['remind_at']

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        return TaskReminder.objects.filter(
            task_id=task_id,
            task__tenant=self.request.user.tenant
        )

    def perform_create(self, serializer):
        task = generics.get_object_or_404(
            Task.objects.filter(tenant=self.request.user.tenant),
            pk=self.kwargs.get('task_id')
        )
        serializer.save(task=task)

class TaskReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskReminderSerializer
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]
    lookup_field = 'pk'

    def get_queryset(self):
        return TaskReminder.objects.filter(
            task__tenant=self.request.user.tenant
        )

class TaskDashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(tenant=request.user.tenant)
        
        # Status counts
        status_counts = tasks.values('status').annotate(count=models.Count('id'))
        total = tasks.count()
        
        status_data = []
        for item in status_counts:
            percentage = (item['count'] / total) * 100 if total > 0 else 0
            status_data.append({
                'status': item['status'],
                'count': item['count'],
                'percentage': round(percentage, 2)
            })
        
        # Priority counts
        priority_counts = tasks.values('priority').annotate(count=models.Count('id'))
        
        # Overdue tasks
        overdue = tasks.filter(
            due_date__lt=timezone.now(),
            status__in=[Task.Status.PENDING, Task.Status.IN_PROGRESS]
        ).count()
        
        data = {
            'status_counts': status_data,
            'priority_counts': priority_counts,
            'overdue_count': overdue,
            'total_count': total
        }
        
        serializer = TaskDashboardSerializer(data, many=False)
        return Response(serializer.data)

class TaskCompletionStatsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSameTenant]

    def get(self, request, *args, **kwargs):
        from django.db.models.functions import TruncDate
        from django.db.models import Count
        
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=days)
        
        # Completed tasks by day
        completed = Task.objects.filter(
            tenant=request.user.tenant,
            status=Task.Status.COMPLETED,
            completed_at__gte=start_date,
            completed_at__lte=end_date
        ).annotate(
            date=TruncDate('completed_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        # Created tasks by day
        created = Task.objects.filter(
            tenant=request.user.tenant,
            created_at__gte=start_date,
            created_at__lte=end_date
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        # Convert to dict for easier processing
        completed_dict = {item['date']: item['count'] for item in completed}
        created_dict = {item['date']: item['count'] for item in created}
        
        # Generate all dates in range
        date_list = [start_date + timedelta(days=x) for x in range(days + 1)]
        
        # Build response data
        stats = []
        for date in date_list:
            stats.append({
                'date': date.date(),
                'completed': completed_dict.get(date.date(), 0),
                'created': created_dict.get(date.date(), 0)
            })
        
        serializer = TaskCompletionStatsSerializer(stats, many=True)
        return Response(serializer.data)
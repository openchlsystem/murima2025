from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Task, TaskTag, TaskTagging, TaskComment,
    TaskAttachment, TaskReminder, TaskChangeLog
)
from apps.tenant.cases.serializers import CaseDetailSerializer  
from workflows.serializers import WorkflowSerializer  
from users.serializers import UserSerializer  

User = get_user_model()


class TaskTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTag
        fields = ['id', 'name', 'color', 'description']
        read_only_fields = ['id']


class TaskTaggingSerializer(serializers.ModelSerializer):
    tag = TaskTagSerializer(read_only=True)
    tag_id = serializers.PrimaryKeyRelatedField(
        queryset=TaskTag.objects.all(),
        source='tag',
        write_only=True
    )

    class Meta:
        model = TaskTagging
        fields = ['id', 'tag', 'tag_id', 'created_at']
        read_only_fields = ['id', 'tag', 'created_at']


class TaskCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = TaskComment
        fields = [
            'id', 'task', 'author', 'author_id', 'content',
            'created_at', 'updated_at', 'is_system_note'
        ]
        read_only_fields = [
            'id', 'author', 'created_at', 'updated_at', 'is_system_note'
        ]
        extra_kwargs = {
            'task': {'write_only': True}
        }

    def create(self, validated_data):
        # Set the current user as author if not specified
        if 'author' not in validated_data or not validated_data['author']:
            validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class TaskAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = TaskAttachment
        fields = [
            'id', 'task', 'file', 'file_url', 'file_name', 'file_size',
            'uploaded_by', 'uploaded_at', 'description'
        ]
        read_only_fields = [
            'id', 'uploaded_by', 'uploaded_at', 'file_url',
            'file_name', 'file_size'
        ]
        extra_kwargs = {
            'task': {'write_only': True},
            'file': {'write_only': True}
        }

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None

    def get_file_name(self, obj):
        if obj.file:
            return obj.file.name.split('/')[-1]
        return None

    def get_file_size(self, obj):
        if obj.file:
            return obj.file.size
        return None

    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class TaskReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskReminder
        fields = ['id', 'task', 'remind_at', 'notified', 'created_at']
        read_only_fields = ['id', 'notified', 'created_at']
        extra_kwargs = {
            'task': {'write_only': True}
        }


class TaskChangeLogSerializer(serializers.ModelSerializer):
    changed_by = UserSerializer(read_only=True)

    class Meta:
        model = TaskChangeLog
        fields = [
            'id', 'task', 'changed_by', 'changed_at',
            'field', 'old_value', 'new_value'
        ]
        read_only_fields = fields


class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    priority_display = serializers.CharField(
        source='get_priority_display',
        read_only=True
    )
    is_overdue = serializers.BooleanField(read_only=True)
    progress = serializers.IntegerField(read_only=True)
    
    # Nested relationships
    created_by = UserSerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='created_by',
        write_only=True,
        required=False,
        allow_null=True
    )
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_to',
        write_only=True,
        required=False,
        allow_null=True
    )
    case = CaseDetailSerializer(read_only=True)
    case_id = serializers.PrimaryKeyRelatedField(
        queryset=Case.objects.all(),
        source='case',
        write_only=True,
        required=False,
        allow_null=True
    )
    workflow = WorkflowSerializer(read_only=True)
    workflow_id = serializers.PrimaryKeyRelatedField(
        queryset=Workflow.objects.all(),
        source='workflow',
        write_only=True,
        required=False,
        allow_null=True
    )
    parent_task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False,
        allow_null=True
    )
    subtasks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all(),
        required=False
    )
    
    # Related fields
    tags = TaskTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TaskTag.objects.all(),
        source='tags',
        write_only=True,
        required=False
    )
    comments = TaskCommentSerializer(many=True, read_only=True)
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    reminders = TaskReminderSerializer(many=True, read_only=True)
    change_logs = TaskChangeLogSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 'priority_display',
            'status', 'status_display', 'due_date', 'created_at', 'updated_at',
            'completed_at', 'is_overdue', 'progress',
            
            # Relationships
            'created_by', 'created_by_id', 'assigned_to', 'assigned_to_id',
            'case', 'case_id', 'workflow', 'workflow_id', 'parent_task',
            'subtasks',
            
            # Related fields
            'tags', 'tag_ids', 'comments', 'attachments', 'reminders',
            'change_logs'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'completed_at', 'is_overdue',
            'progress', 'status_display', 'priority_display'
        ]

    def create(self, validated_data):
        # Handle tag_ids
        tag_ids = validated_data.pop('tags', [])
        
        # Set created_by to current user if not specified
        if 'created_by' not in validated_data or not validated_data['created_by']:
            validated_data['created_by'] = self.context['request'].user
        
        # Create the task
        task = super().create(validated_data)
        
        # Add tags
        if tag_ids:
            task.tags.set(tag_ids)
        
        return task

    def update(self, instance, validated_data):
        # Track who made the changes for audit logging
        instance._changed_by = self.context['request'].user
        
        # Handle tag_ids if provided
        if 'tags' in validated_data:
            tag_ids = validated_data.pop('tags')
            instance.tags.set(tag_ids)
        
        return super().update(instance, validated_data)


class TaskListSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    priority_display = serializers.CharField(
        source='get_priority_display',
        read_only=True
    )
    is_overdue = serializers.BooleanField(read_only=True)
    progress = serializers.IntegerField(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    tags = TaskTagSerializer(many=True, read_only=True)
    case = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'priority', 'priority_display',
            'status', 'status_display', 'due_date', 'created_at',
            'is_overdue', 'progress', 'assigned_to', 'tags', 'case'
        ]
        read_only_fields = fields


class TaskDashboardSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()


class TaskCompletionStatsSerializer(serializers.Serializer):
    date = serializers.DateField()
    completed = serializers.IntegerField()
    created = serializers.IntegerField()
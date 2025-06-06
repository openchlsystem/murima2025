# apps/ai/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AIInteraction, AIPromptTemplate


@admin.register(AIInteraction)
class AIInteractionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'interaction_type', 'model_used', 
        'confidence_score', 'processing_time_ms', 'was_helpful', 'created_at'
    ]
    list_filter = [
        'interaction_type', 'model_used', 'was_helpful', 'created_at'
    ]
    search_fields = ['user__username', 'input_text', 'output_text']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('user', 'interaction_type', 'model_used')
        }),
        (_('Content'), {
            'fields': ('input_text', 'output_text')
        }),
        (_('Metrics'), {
            'fields': ('confidence_score', 'processing_time_ms', 'was_helpful')
        }),
        (_('Additional Data'), {
            'fields': ('context_data',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(AIPromptTemplate)
class AIPromptTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'interaction_type', 'is_active', 'created_at']
    list_filter = ['interaction_type', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'prompt_template']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'description', 'interaction_type', 'is_active')
        }),
        (_('Template'), {
            'fields': ('prompt_template', 'variables')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
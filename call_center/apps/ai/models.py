# apps/ai/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class AIInteraction(TimeStampedModel):
    """Track AI interactions for analytics and improvement"""
    
    INTERACTION_TYPES = [
        ('suggestion', _('Suggestion')),
        ('classification', _('Classification')),
        ('sentiment', _('Sentiment Analysis')),
        ('summary', _('Summary')),
        ('response', _('Response Generation')),
    ]
    
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='ai_interactions',
        verbose_name=_("User")
    )
    interaction_type = models.CharField(
        max_length=20,
        choices=INTERACTION_TYPES,
        verbose_name=_("Interaction Type")
    )
    input_text = models.TextField(
        verbose_name=_("Input Text"),
        help_text=_("The text that was sent to AI")
    )
    output_text = models.TextField(
        verbose_name=_("Output Text"),
        help_text=_("The response from AI")
    )
    confidence_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Confidence Score"),
        help_text=_("AI confidence score (0.0 to 1.0)")
    )
    processing_time_ms = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Processing Time (ms)")
    )
    model_used = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Model Used"),
        help_text=_("Which AI model was used")
    )
    context_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Context Data"),
        help_text=_("Additional context data for the interaction")
    )
    was_helpful = models.BooleanField(
        null=True,
        blank=True,
        verbose_name=_("Was Helpful"),
        help_text=_("User feedback on whether the AI response was helpful")
    )
    
    class Meta:
        verbose_name = _("AI Interaction")
        verbose_name_plural = _("AI Interactions")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['interaction_type', '-created_at']),
            models.Index(fields=['model_used']),
        ]
    
    def __str__(self):
        return f"{self.get_interaction_type_display()} - {self.user.username} - {self.created_at}"


class AIPromptTemplate(TimeStampedModel):
    """Store reusable AI prompt templates"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    prompt_template = models.TextField(
        verbose_name=_("Prompt Template"),
        help_text=_("Template with placeholders like {variable_name}")
    )
    interaction_type = models.CharField(
        max_length=20,
        choices=AIInteraction.INTERACTION_TYPES,
        verbose_name=_("Interaction Type")
    )
    variables = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Variables"),
        help_text=_("List of variable names used in the template")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active")
    )
    
    class Meta:
        verbose_name = _("AI Prompt Template")
        verbose_name_plural = _("AI Prompt Templates")
        ordering = ['name']
    
    def __str__(self):
        return self.name
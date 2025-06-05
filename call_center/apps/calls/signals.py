# apps/calls/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Call, CallEvent


@receiver(pre_save, sender=Call)
def call_pre_save(sender, instance, **kwargs):
    """Calculate derived fields before saving"""
    if instance.start_time:
        instance.call_date = instance.start_time.date()
        instance.call_hour = instance.start_time.hour
        instance.call_day_of_week = instance.start_time.weekday()


@receiver(post_save, sender=Call)
def call_post_save(sender, instance, created, **kwargs):
    """Handle post-save logic for calls"""
    if created:
        # Create initial call event
        CallEvent.objects.create(
            call=instance,
            event_type='dial',
            event_time=instance.start_time,
            description='Call initiated',
            agent=instance.agent
        )
        
        # If call was answered, create answer event
        if instance.answer_time:
            CallEvent.objects.create(
                call=instance,
                event_type='answer',
                event_time=instance.answer_time,
                description='Call answered',
                agent=instance.agent
            )
        
        # If call ended, create hangup event
        if instance.end_time:
            CallEvent.objects.create(
                call=instance,
                event_type='hangup',
                event_time=instance.end_time,
                description=f'Call ended: {instance.hangup_reason}',
                agent=instance.agent
            )
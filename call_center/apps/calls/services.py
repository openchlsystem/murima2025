# apps/calls/services.py
from django.db import transaction
from django.utils import timezone

class CallService:
    """Service for call management."""
    
    @staticmethod
    @transaction.atomic
    def create_call(unique_id, caller_number, direction, campaign=None, **kwargs):
        """
        Create a new call record.
        
        Args:
            unique_id: Unique identifier for the call
            caller_number: Phone number of the caller
            direction: Call direction ('inbound', 'outbound', 'internal')
            campaign: Optional Campaign object
            **kwargs: Additional call fields
            
        Returns:
            Newly created Call object
        """
        from apps.calls.models import Call
        from apps.contacts.models import Contact
        
        # Check if contact exists for this number
        contact = Contact.objects.filter(phone=caller_number).first()
        
        # Create the call
        call = Call.objects.create(
            unique_id=unique_id,
            caller_number=caller_number,
            direction=direction,
            campaign=campaign,
            contact=contact,
            start_time=timezone.now(),
            status='ringing',
            **kwargs
        )
        
        return call
    
    @staticmethod
    @transaction.atomic
    def record_call_event(call_id, event_type, agent=None, details=None):
        """
        Record a call event.
        
        Args:
            call_id: ID of the call
            event_type: Type of event ('queued', 'ringing', 'answered', etc.)
            agent: Optional User object for the agent
            details: Optional JSON details for the event
            
        Returns:
            Newly created CallEvent object
        """
        from apps.calls.models import Call, CallEvent
        
        call = Call.objects.get(id=call_id)
        
        event = CallEvent.objects.create(
            call=call,
            event_type=event_type,
            event_time=timezone.now(),
            agent=agent,
            details=details
        )
        
        # Update the call status based on the event
        if event_type == 'answered':
            call.status = 'answered'
            call.answer_time = event.event_time
            call.agent = agent
            
        elif event_type == 'hangup':
            call.status = details.get('status', 'answered') if details else 'answered'
            call.end_time = event.event_time
            call.hangup_reason = details.get('reason') if details else None
            
            # Calculate duration
            if call.start_time:
                call.duration_seconds = (event.event_time - call.start_time).total_seconds()
            
            # Calculate talk time
            if call.answer_time:
                call.talk_time_seconds = (event.event_time - call.answer_time).total_seconds()
            
        call.save()
        
        return event
    
    @staticmethod
    @transaction.atomic
    def end_call(call_id, status='answered', hangup_reason=None):
        """
        End a call.
        
        Args:
            call_id: ID of the call
            status: Final status of the call
            hangup_reason: Optional hangup reason
            
        Returns:
            Updated Call object
        """
        from apps.calls.models import Call
        
        call = Call.objects.get(id=call_id)
        now = timezone.now()
        
        call.status = status
        call.end_time = now
        call.hangup_reason = hangup_reason
        
        # Calculate durations
        if call.start_time:
            call.duration_seconds = (now - call.start_time).total_seconds()
            
        if call.answer_time:
            call.talk_time_seconds = (now - call.answer_time).total_seconds()
            
        call.save()
        
        # Record the hangup event
        CallService.record_call_event(
            call_id=call.id,
            event_type='hangup',
            agent=call.agent,
            details={
                'status': status,
                'reason': hangup_reason
            }
        )
        
        return call
    
    @staticmethod
    @transaction.atomic
    def create_case_from_call(call_id, user, reporter=None, **case_kwargs):
        """
        Create a new case from a call.
        
        Args:
            call_id: ID of the call
            user: User creating the case
            reporter: Optional Contact object for the reporter (uses call.contact if not provided)
            **case_kwargs: Additional case fields
            
        Returns:
            Tuple of (Call, Case) objects
        """
        from apps.calls.models import Call
        from apps.cases.services import CaseService
        from apps.contacts.models import Contact
        
        call = Call.objects.get(id=call_id)
        
        # If no reporter provided, use the call contact or create a new one
        if not reporter:
            if call.contact:
                reporter = call.contact
            else:
                # Create a new contact from the call info
                reporter = Contact.objects.create(
                    phone=call.caller_number,
                    full_name=call.caller_name,
                    created_by=user
                )
                
                # Update the call with the new contact
                call.contact = reporter
                call.save()
        
        # Create the case
        case = CaseService.create_case(
            reporter=reporter,
            source=f'call:{call.direction}',
            user=user,
            **case_kwargs
        )
        
        # Link the call to the case
        call.case = case
        call.save()
        
        return call, case
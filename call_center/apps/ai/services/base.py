# apps/ai/services/base.py
import abc
import time
import logging
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from apps.ai.models import AIInteraction, AIProvider

logger = logging.getLogger(__name__)

class BaseAIService(abc.ABC):
    """Abstract base class for AI service implementations."""
    
    def __init__(self, provider_name=None):
        """
        Initialize with optional specific provider.
        
        Args:
            provider_name (str, optional): Specific provider name to use.
                                          If None, use default provider.
        """
        if provider_name:
            self.provider = AIProvider.objects.filter(
                name=provider_name, 
                is_active=True
            ).first()
        else:
            self.provider = AIProvider.objects.filter(
                is_default=True, 
                is_active=True
            ).first()
            
        if not self.provider:
            raise ValueError("No active AI provider found")
    
    @abc.abstractmethod
    def generate_response(self, prompt, model=None, temperature=0.7, max_tokens=None):
        """
        Generate AI response for the given prompt.
        
        Args:
            prompt (str): The prompt text
            model (str, optional): Override the default model
            temperature (float): Controls randomness (0-1)
            max_tokens (int, optional): Maximum tokens to generate
            
        Returns:
            dict: The AI response
        """
        pass
    
    def record_interaction(self, content_object, interaction_type, prompt, response, 
                           execution_time_ms, token_count=None, user=None):
        """
        Record an AI interaction for auditing.
        
        Args:
            content_object: The Django model instance this interaction relates to
            interaction_type (str): Type of interaction
            prompt (str): The prompt sent to the AI
            response (dict): The response from the AI
            execution_time_ms (int): Execution time in milliseconds
            token_count (int, optional): Number of tokens used
            user (User, optional): The user who initiated this interaction
            
        Returns:
            AIInteraction: The created interaction record
        """
        content_type = ContentType.objects.get_for_model(content_object)
        
        interaction = AIInteraction.objects.create(
            content_type=content_type,
            object_id=content_object.id,
            interaction_type=interaction_type,
            prompt=prompt,
            response=response,
            provider=self.provider,
            execution_time_ms=execution_time_ms,
            token_count=token_count,
            user=user
        )
        
        return interaction
    
    def process_with_tracking(self, content_object, interaction_type, prompt, 
                              model=None, temperature=0.7, max_tokens=None, user=None):
        """
        Process an AI request with tracking.
        
        Args:
            content_object: The Django model instance this interaction relates to
            interaction_type (str): Type of interaction
            prompt (str): The prompt to send
            model (str, optional): Override the default model
            temperature (float): Controls randomness (0-1)
            max_tokens (int, optional): Maximum tokens to generate
            user (User, optional): The user who initiated this
            
        Returns:
            dict: The AI response
        """
        start_time = time.time()
        
        try:
            response = self.generate_response(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Extract token count if available
            token_count = response.get('usage', {}).get('total_tokens')
            
            # Record the interaction
            self.record_interaction(
                content_object=content_object,
                interaction_type=interaction_type,
                prompt=prompt,
                response=response,
                execution_time_ms=execution_time_ms,
                token_count=token_count,
                user=user
            )
            
            return response
            
        except Exception as e:
            logger.error(f"AI processing error: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "success": False
            }
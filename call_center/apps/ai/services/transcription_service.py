# apps/ai/services/openai_service.py
import openai # type: ignore
from django.conf import settings
from .base import BaseAIService

class OpenAIService(BaseAIService):
    """Service for OpenAI (GPT) integration."""
    
    def __init__(self, provider_name=None):
        super().__init__(provider_name)
        openai.api_key = self.provider.api_key
        
        # Use custom API URL if specified
        if self.provider.api_url:
            openai.api_base = self.provider.api_url
    
    def generate_response(self, prompt, model=None, temperature=0.7, max_tokens=None):
        """
        Generate response from OpenAI.
        
        Args:
            prompt (str): The prompt text
            model (str, optional): Override the default model
            temperature (float): Controls randomness (0-1)
            max_tokens (int, optional): Maximum tokens to generate
            
        Returns:
            dict: The OpenAI response
        """
        # Use provider default model if not specified
        model = model or self.provider.model_name or "gpt-4"
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return response
# apps/ai/services/case_service.py
# from .openai_service import OpenAIService # type: ignore
from apps.ai.models import PromptTemplate
from django.template import Template, Context

class CaseAIService:
    """AI services specific to case management."""
    
    @staticmethod
    def get_case_suggestions(case, user=None):
        """
        Get AI suggestions for case information.
        
        Args:
            case: The Case object
            user: The User requesting suggestions
            
        Returns:
            dict: Suggestions from AI
        """
        # Get the appropriate template
        template = PromptTemplate.objects.filter(
            name='case_suggestions',
            is_active=True
        ).first()
        
        if not template:
            # Fallback if no template in database
            prompt_text = f"""
            Based on the following case information, provide:
            1. Potential case categories
            2. Suggested services to offer
            3. Potential referrals
            4. Questions to ask for further information
            
            Case Number: {case.case_number}
            Reporter: {case.reporter.full_name if case.reporter else 'Unknown'}
            Category: {case.category.name if case.category else 'Unknown'}
            Narrative: {case.narrative or ''}
            """
        else:
            # Use the template from the database
            django_template = Template(template.template)
            context = Context({
                'case': case,
                'reporter': case.reporter,
                'narrative': case.narrative,
                'category': case.category,
            })
            prompt_text = django_template.render(context)
        
        # Initialize OpenAI service
        ai_service = OpenAIService()
        
        # Process with tracking
        response = ai_service.process_with_tracking(
            content_object=case,
            interaction_type='suggestion',
            prompt=prompt_text,
            temperature=0.3,  # Lower temperature for more focused results
            user=user
        )
        
        if 'error' in response:
            return {
                'success': False,
                'error': response['error'],
                'suggestions': []
            }
        
        # Extract the content from the response
        assistant_message = response.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        # Return a structured response
        return {
            'success': True,
            'text': assistant_message,
            'case_id': case.id,
            'prompt': prompt_text
        }

    @staticmethod
    def categorize_case(case, narrative=None, user=None):
        """
        Suggest categories for a case based on narrative.
        
        Args:
            case: The Case object
            narrative: Optional narrative text (overrides case.narrative)
            user: The User requesting categorization
            
        Returns:
            dict: Suggested categories
        """
        # Get text to analyze
        text_to_analyze = narrative or case.narrative
        
        if not text_to_analyze:
            return {
                'success': False,
                'error': 'No narrative provided for categorization',
                'categories': []
            }
        
        # Get available categories for reference
        from apps.core.models import ReferenceData
        categories = list(ReferenceData.objects.filter(
            category='case_category',
            is_active=True
        ).values_list('name', flat=True))
        
        # Create the prompt
        prompt_text = f"""
        Based on the following case narrative, suggest the most appropriate category.
        Available categories: {', '.join(categories)}
        
        Narrative:
        {text_to_analyze}
        
        Return your answer in JSON format with the following structure:
        {{
            "primary_category": "The most appropriate category",
            "confidence": 0.95,
            "alternative_categories": ["Second best match", "Third best match"],
            "reasoning": "Brief explanation of your categorization"
        }}
        """
        
        # Initialize OpenAI service
        ai_service = OpenAIService()
        
        # Process with tracking
        response = ai_service.process_with_tracking(
            content_object=case,
            interaction_type='classification',
            prompt=prompt_text,
            temperature=0.2,  # Low temperature for more deterministic results
            user=user
        )
        
        if 'error' in response:
            return {
                'success': False,
                'error': response['error'],
                'categories': []
            }
        
        # Extract the content
        content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        # Try to parse JSON from the response
        import json
        try:
            # Find JSON in the response
            import re
            json_match = re.search(r'({.*})', content.replace('\n', ''))
            if json_match:
                result = json.loads(json_match.group(0))
                return {
                    'success': True,
                    'categories': result
                }
            else:
                return {
                    'success': False,
                    'error': 'Could not parse AI response',
                    'raw_response': content
                }
        except json.JSONDecodeError:
            return {
                'success': False,
                'error': 'Invalid JSON in AI response',
                'raw_response': content
            }
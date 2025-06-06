# apps/api/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import IntegrityError
import logging

logger = logging.getLogger(__name__)

class ServiceException(APIException):
    """Custom exception for service layer errors."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A service error occurred.'
    default_code = 'service_error'

def custom_exception_handler(exc, context):
    """Handle exceptions with standardized responses."""
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If response is None, then Django doesn't recognize this exception
    if response is None:
        if isinstance(exc, DjangoValidationError):
            # Handle Django validation errors
            if hasattr(exc, 'message_dict'):
                data = {'detail': exc.message_dict}
            else:
                data = {'detail': exc.messages}
                
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        elif isinstance(exc, IntegrityError):
            # Handle database integrity errors
            return Response(
                {'detail': 'Database integrity error occurred.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # Log the error for unexpected exceptions
            logger.error(f'Unhandled exception: {str(exc)}')
            return Response(
                {'detail': 'A server error occurred.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return response
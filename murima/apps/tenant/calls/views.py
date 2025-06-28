from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Extension, CallLog
from .serializers import (
    ExtensionSerializer, 
    ExtensionRetrieveSerializer,
    CallLogSerializer
)
from .services.ari_client import ARIClient
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class CallLogPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['POST'])
def create_extension(request):
    """
    Create extension for a user
    POST /api/extensions/
    Payload: {"user_id": 123, "username": "1001", "password": "1001pass"}
    """
    serializer = ExtensionSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            # Save extension to database
            extension = serializer.save()
            
            # Create extension in Asterisk via ARI
            ari_client = ARIClient()
            ari_success = ari_client.create_extension(
                extension.username, 
                extension.password
            )
            
            if not ari_success:
                # If ARI creation fails, delete the database record
                extension.delete()
                return Response(
                    {"error": "Failed to create extension in Asterisk"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response(
                {
                    "message": "Extension created successfully",
                    "extension": {
                        "id": extension.id,
                        "username": extension.username,
                        "user_id": extension.user.id
                    }
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"Error creating extension: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_extension(request, user_id):
    """
    Get extension credentials for a user (for WebRTC registration)
    GET /api/extensions/user/{user_id}/
    """
    try:
        user = get_object_or_404(User, id=user_id)
        extension = get_object_or_404(Extension, user=user)
        
        serializer = ExtensionRetrieveSerializer(extension)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving extension for user {user_id}: {str(e)}")
        return Response(
            {"error": "Extension not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def get_user_call_logs(request, user_id):
    """
    Get call logs for a user
    GET /api/call-logs/user/{user_id}/
    """
    try:
        user = get_object_or_404(User, id=user_id)
        
        # Get user's extension
        try:
            extension = Extension.objects.get(user=user)
        except Extension.DoesNotExist:
            return Response(
                {"error": "User does not have an extension"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get call logs where user is either caller or callee
        call_logs = CallLog.objects.filter(
            Q(caller_extension=extension) | Q(callee_extension=extension)
        ).select_related('caller_extension', 'callee_extension', 'caller_extension__user', 'callee_extension__user')
        
        # Apply pagination
        paginator = CallLogPagination()
        paginated_logs = paginator.paginate_queryset(call_logs, request)
        
        serializer = CallLogSerializer(paginated_logs, many=True)
        
        return paginator.get_paginated_response({
            "call_logs": serializer.data,
            "total": call_logs.count()
        })
        
    except Exception as e:
        logger.error(f"Error retrieving call logs for user {user_id}: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def extension_status(request, extension_id):
    """
    Check extension status
    GET /api/extensions/{extension_id}/status/
    """
    try:
        extension = get_object_or_404(Extension, id=extension_id)
        
        # Check if extension is registered in Asterisk
        ari_client = ARIClient()
        is_registered = ari_client.check_extension_status(extension.username)
        
        return Response({
            "extension_id": extension.id,
            "username": extension.username,
            "is_active": extension.is_active,
            "is_registered": is_registered
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error checking extension status: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
def delete_extension(request, extension_id):
    """
    Delete extension
    DELETE /api/extensions/{extension_id}/
    """
    try:
        extension = get_object_or_404(Extension, id=extension_id)
        
        # Remove from Asterisk first
        ari_client = ARIClient()
        ari_success = ari_client.delete_extension(extension.username)
        
        if ari_success:
            extension.delete()
            return Response(
                {"message": "Extension deleted successfully"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Failed to delete extension from Asterisk"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Error deleting extension: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
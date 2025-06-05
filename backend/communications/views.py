# core/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Channel, Contact, Message, Conversation,
    Tag, CallLog, Template
)
from .serializers import (
    ChannelSerializer, ContactSerializer, MessageSerializer,
    ConversationSerializer, TagSerializer, CallLogSerializer,
    TemplateSerializer
)
from .permissions import IsTenantMember

class ChannelListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Channel.objects.filter(tenant=self.request.user.tenant)
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class ChannelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Channel.objects.filter(tenant=self.request.user.tenant)

class ContactListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Contact.objects.filter(tenant=self.request.user.tenant)
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class ContactRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Contact.objects.filter(tenant=self.request.user.tenant)

class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Message.objects.filter(channel__tenant=self.request.user.tenant)
    
    def perform_create(self, serializer):
        # Ensure the channel belongs to the tenant
        channel = get_object_or_404(
            Channel, 
            id=serializer.validated_data['channel'].id,
            tenant=self.request.user.tenant
        )
        serializer.save(channel=channel)

class MessageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Message.objects.filter(channel__tenant=self.request.user.tenant)

class ConversationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Conversation.objects.filter(tenant=self.request.user.tenant)
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class ConversationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Conversation.objects.filter(tenant=self.request.user.tenant)

class TagListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Tag.objects.filter(tenant=self.request.user.tenant)
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class TagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Tag.objects.filter(tenant=self.request.user.tenant)

class CallLogListAPIView(generics.ListAPIView):
    serializer_class = CallLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return CallLog.objects.filter(channel__tenant=self.request.user.tenant)

class CallLogRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CallLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return CallLog.objects.filter(channel__tenant=self.request.user.tenant)

class TemplateListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Template.objects.filter(tenant=self.request.user.tenant)
    
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class TemplateRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsTenantMember]
    
    def get_queryset(self):
        return Template.objects.filter(tenant=self.request.user.tenant)
    
    
    
    


# Asterisks API

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .asterisks.ari_client import ARIClient

ari = ARIClient()

@csrf_exempt
def originate_call(request):
    if request.method == 'POST':
        endpoint = request.POST.get('endpoint')  # e.g., "PJSIP/1001"
        extension = request.POST.get('extension')  # e.g., "1002"
        result = ari.originate_call(endpoint, extension)
        return JsonResponse(result)
    return JsonResponse({'error': 'POST required'})

def handle_ari_event(event):
    """Process ARI events (e.g., call answered, hung up)."""
    print("ARI Event:", event)
    # Add your logic here (e.g., update database, trigger actions)
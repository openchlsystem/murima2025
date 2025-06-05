# core/urls.py
from django.urls import path
from .views import (
    ChannelListCreateAPIView, ChannelRetrieveUpdateDestroyAPIView,
    ContactListCreateAPIView, ContactRetrieveUpdateDestroyAPIView,
    MessageListCreateAPIView, MessageRetrieveUpdateDestroyAPIView,
    ConversationListCreateAPIView, ConversationRetrieveUpdateDestroyAPIView,
    TagListCreateAPIView, TagRetrieveUpdateDestroyAPIView,
    CallLogListAPIView, CallLogRetrieveAPIView,
    TemplateListCreateAPIView, TemplateRetrieveUpdateDestroyAPIView,originate_call
)

urlpatterns = [
    # Channels
    path('channels/', ChannelListCreateAPIView.as_view(), name='channel-list'),
    path('channels/<int:pk>/', ChannelRetrieveUpdateDestroyAPIView.as_view(), name='channel-detail'),
    
    # Contacts
    path('contacts/', ContactListCreateAPIView.as_view(), name='contact-list'),
    path('contacts/<int:pk>/', ContactRetrieveUpdateDestroyAPIView.as_view(), name='contact-detail'),
    
    # Messages
    path('messages/', MessageListCreateAPIView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyAPIView.as_view(), name='message-detail'),
    
    # Conversations
    path('conversations/', ConversationListCreateAPIView.as_view(), name='conversation-list'),
    path('conversations/<int:pk>/', ConversationRetrieveUpdateDestroyAPIView.as_view(), name='conversation-detail'),
    
    # Tags
    path('tags/', TagListCreateAPIView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagRetrieveUpdateDestroyAPIView.as_view(), name='tag-detail'),
    
    # Call Logs (read-only)
    path('call-logs/', CallLogListAPIView.as_view(), name='call-log-list'),
    path('call-logs/<int:pk>/', CallLogRetrieveAPIView.as_view(), name='call-log-detail'),
    
    # Templates
    path('templates/', TemplateListCreateAPIView.as_view(), name='template-list'),
    path('templates/<int:pk>/', TemplateRetrieveUpdateDestroyAPIView.as_view(), name='template-detail'),
    
    
    # ARI (Automated Response Interface) URLs
     path('originate_call/', originate_call, name='originate_call'),
]
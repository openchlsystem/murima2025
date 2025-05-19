from django.urls import path
from .views import (
    ChannelListCreateView,
    ChannelRetrieveUpdateDestroyView,
    MessageListCreateView
)

urlpatterns = [
    # Channels
    path('channels/', ChannelListCreateView.as_view(), name='channel-list-create'),
    path('channels/<int:pk>/', ChannelRetrieveUpdateDestroyView.as_view(), name='channel-detail'),
    
    # Messages
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
]
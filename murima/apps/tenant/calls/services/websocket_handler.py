import asyncio
import websockets
import json
import logging
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from ..models import Extension, CallLog

logger = logging.getLogger(__name__)


class ARIWebSocketHandler:
    """
    Handles WebSocket connection to Asterisk ARI for real-time call events
    """
    
    def __init__(self):
        self.ari_ws_url = getattr(settings, 'ASTERISK_ARI_WS_URL', 'ws://localhost:8088/ari/events')
        self.ari_username = getattr(settings, 'ASTERISK_ARI_USERNAME', 'ari_user')
        self.ari_password = getattr(settings, 'ASTERISK_ARI_PASSWORD', 'ari_password')
        self.app_name = getattr(settings, 'ASTERISK_ARI_APP', 'django_calls')
        
        # Track active calls
        self.active_calls = {}
        
    async def connect_and_listen(self):
        """
        Connect to ARI WebSocket and listen for events
        """
        uri = f"{self.ari_ws_url}?app={self.app_name}&api_key={self.ari_username}:{self.ari_password}"
        
        while True:
            try:
                logger.info("Connecting to Asterisk ARI WebSocket...")
                
                async with websockets.connect(uri) as websocket:
                    logger.info("Connected to Asterisk ARI WebSocket")
                    
                    async for message in websocket:
                        try:
                            event_data = json.loads(message)
                            await self.handle_event(event_data)
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse WebSocket message: {message}")
                        except Exception as e:
                            logger.error(f"Error handling WebSocket event: {str(e)}")
                            
            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket connection closed, reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"WebSocket connection error: {str(e)}")
                await asyncio.sleep(10)

    async def handle_event(self, event_data):
        """
        Handle different types of ARI events
        """
        event_type = event_data.get('type')
        
        if event_type == 'StasisStart':
            await self.handle_stasis_start(event_data)
        elif event_type == 'StasisEnd':
            await self.handle_stasis_end(event_data)
        elif event_type == 'ChannelStateChange':
            await self.handle_channel_state_change(event_data)
        elif event_type == 'ChannelDestroyed':
            await self.handle_channel_destroyed(event_data)
        elif event_type == 'Dial':
            await self.handle_dial_event(event_data)
        elif event_type == 'DialEnd':
            await self.handle_dial_end(event_data)
        else:
            logger.debug(f"Unhandled event type: {event_type}")

    async def handle_stasis_start(self, event_data):
        """
        Handle when a call enters the Stasis application
        """
        try:
            channel = event_data.get('channel', {})
            channel_id = channel.get('id')
            caller_id = channel.get('caller', {}).get('number')
            
            logger.info(f"Call started - Channel: {channel_id}, Caller: {caller_id}")
            
            # Extract extension information
            caller_extension = self.extract_extension_from_channel(channel)
            
            if caller_extension and channel_id:
                self.active_calls[channel_id] = {
                    'caller_extension': caller_extension,
                    'start_time': timezone.now(),
                    'channel_id': channel_id,
                    'status': 'ringing',
                    'caller_channel': channel_id
                }
                
        except Exception as e:
            logger.error(f"Error handling StasisStart: {str(e)}")

    async def handle_stasis_end(self, event_data):
        """
        Handle when a call leaves the Stasis application
        """
        try:
            channel = event_data.get('channel', {})
            channel_id = channel.get('id')
            
            if channel_id in self.active_calls:
                call_data = self.active_calls[channel_id]
                call_data['end_time'] = timezone.now()
                
                logger.info(f"Call ended - Channel: {channel_id}")
                
                # Create call log entry if we have complete call information
                if call_data.get('callee_extension'):
                    await self.create_call_log(call_data)
                
                # Remove from active calls
                del self.active_calls[channel_id]
                
        except Exception as e:
            logger.error(f"Error handling StasisEnd: {str(e)}")

    async def handle_channel_state_change(self, event_data):
        """
        Handle channel state changes (ringing, answered, etc.)
        """
        try:
            channel = event_data.get('channel', {})
            channel_id = channel.get('id')
            channel_state = channel.get('state')
            
            if channel_id in self.active_calls:
                if channel_state == 'Up':
                    self.active_calls[channel_id]['status'] = 'answered'
                    self.active_calls[channel_id]['answer_time'] = timezone.now()
                elif channel_state == 'Busy':
                    self.active_calls[channel_id]['status'] = 'busy'
                elif channel_state == 'Ring':
                    self.active_calls[channel_id]['status'] = 'ringing'
                    
                logger.debug(f"Channel {channel_id} state changed to {channel_state}")
                
        except Exception as e:
            logger.error(f"Error handling ChannelStateChange: {str(e)}")

    async def handle_dial_event(self, event_data):
        """
        Handle dial events to capture callee information
        """
        try:
            caller_channel = event_data.get('caller', {})
            peer_channel = event_data.get('peer', {})
            
            caller_channel_id = caller_channel.get('id')
            peer_channel_id = peer_channel.get('id')
            
            # Extract callee extension from peer channel
            callee_extension = self.extract_extension_from_channel(peer_channel)
            
            # Update active call with callee information
            if caller_channel_id in self.active_calls and callee_extension:
                self.active_calls[caller_channel_id]['callee_extension'] = callee_extension
                self.active_calls[caller_channel_id]['peer_channel'] = peer_channel_id
                
                logger.info(f"Dial event: {self.active_calls[caller_channel_id]['caller_extension']} -> {callee_extension}")
                
        except Exception as e:
            logger.error(f"Error handling Dial event: {str(e)}")

    async def handle_dial_end(self, event_data):
        """
        Handle dial end events
        """
        try:
            caller_channel = event_data.get('caller', {})
            peer_channel = event_data.get('peer', {})
            dial_status = event_data.get('dialstatus', 'UNKNOWN')
            
            caller_channel_id = caller_channel.get('id')
            
            if caller_channel_id in self.active_calls:
                # Map dial status to our call status
                status_map = {
                    'ANSWER': 'answered',
                    'BUSY': 'busy',
                    'NOANSWER': 'no_answer',
                    'CANCEL': 'cancelled',
                    'CONGESTION': 'failed',
                    'CHANUNAVAIL': 'failed'
                }
                
                final_status = status_map.get(dial_status, 'failed')
                self.active_calls[caller_channel_id]['final_status'] = final_status
                
                logger.info(f"Dial ended: {caller_channel_id}, Status: {dial_status} -> {final_status}")
                
        except Exception as e:
            logger.error(f"Error handling DialEnd: {str(e)}")

    async def handle_channel_destroyed(self, event_data):
        """
        Handle when a channel is destroyed
        """
        try:
            channel = event_data.get('channel', {})
            channel_id = channel.get('id')
            cause = event_data.get('cause', 0)
            cause_txt = event_data.get('cause_txt', 'Unknown')
            
            if channel_id in self.active_calls:
                call_data = self.active_calls[channel_id]
                call_data['end_time'] = timezone.now()
                call_data['hangup_cause'] = cause_txt
                call_data['hangup_cause_code'] = cause
                
                # Determine call status based on hangup cause if not already set
                if 'final_status' not in call_data:
                    if cause == 16:  # Normal call clearing
                        call_data['final_status'] = 'answered'
                    elif cause == 17:  # User busy
                        call_data['final_status'] = 'busy'
                    elif cause == 19:  # No answer
                        call_data['final_status'] = 'no_answer'
                    elif cause == 21:  # Call rejected
                        call_data['final_status'] = 'cancelled'
                    else:
                        call_data['final_status'] = 'failed'
                
                logger.info(f"Channel destroyed - {channel_id}, Cause: {cause_txt} ({cause})")
                
                # Create call log if we have complete information
                if call_data.get('callee_extension'):
                    await self.create_call_log(call_data)
                
                # Remove from active calls
                del self.active_calls[channel_id]
                
        except Exception as e:
            logger.error(f"Error handling ChannelDestroyed: {str(e)}")

    def extract_extension_from_channel(self, channel):
        """
        Extract extension number from channel information
        """
        try:
            # First try to get from caller number
            caller_number = channel.get('caller', {}).get('number')
            if caller_number and caller_number.isdigit():
                return caller_number
                
            # Alternative: extract from channel name
            channel_name = channel.get('name', '')
            if 'PJSIP/' in channel_name:
                # Extract extension from PJSIP/1001-00000001 format
                parts = channel_name.split('/')
                if len(parts) > 1:
                    extension_part = parts[1].split('-')[0]
                    if extension_part.isdigit():
                        return extension_part
            
            # Try connected line number
            connected_number = channel.get('connected', {}).get('number')
            if connected_number and connected_number.isdigit():
                return connected_number
                
            return None
            
        except Exception as e:
            logger.error(f"Error extracting extension from channel: {str(e)}")
            return None

    async def create_call_log(self, call_data):
        """
        Create call log entry in database
        """
        try:
            caller_extension_username = call_data.get('caller_extension')
            callee_extension_username = call_data.get('callee_extension')
            
            if not caller_extension_username or not callee_extension_username:
                logger.warning(f"Missing extension information for call log: caller={caller_extension_username}, callee={callee_extension_username}")
                return
            
            # Get extension objects
            try:
                caller_extension = await self.get_extension_async(caller_extension_username)
                callee_extension = await self.get_extension_async(callee_extension_username)
                
                if not caller_extension or not callee_extension:
                    logger.error(f"Extension not found: caller={caller_extension_username}, callee={callee_extension_username}")
                    return
                    
            except Exception as e:
                logger.error(f"Error getting extensions: {str(e)}")
                return
            
            # Calculate duration
            start_time = call_data.get('start_time')
            end_time = call_data.get('end_time', timezone.now())
            duration = int((end_time - start_time).total_seconds()) if start_time else 0
            
            # Create call log
            call_log_data = {
                'caller_extension': caller_extension,
                'callee_extension': callee_extension,
                'start_time': start_time,
                'end_time': end_time,
                'duration': duration,
                'call_status': call_data.get('final_status', call_data.get('status', 'failed')),
                'asterisk_call_id': call_data.get('channel_id', '')
            }
            
            # Create the call log using Django ORM in a thread-safe way
            await self.create_call_log_async(call_log_data)
            
            logger.info(f"Call log created: {caller_extension_username} -> {callee_extension_username}")
            
        except Exception as e:
            logger.error(f"Error creating call log: {str(e)}")

    async def get_extension_async(self, username):
        """
        Get extension from database asynchronously
        """
        try:
            from django.db import connection
            from asgiref.sync import sync_to_async
            
            # Use sync_to_async to make the database query async-safe
            get_extension = sync_to_async(Extension.objects.get)
            return await get_extension(username=username)
            
        except Extension.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting extension {username}: {str(e)}")
            return None

    async def create_call_log_async(self, call_log_data):
        """
        Create call log asynchronously
        """
        try:
            from asgiref.sync import sync_to_async
            
            # Use sync_to_async to make the database operation async-safe
            create_call_log = sync_to_async(CallLog.objects.create)
            call_log = await create_call_log(**call_log_data)
            return call_log
            
        except Exception as e:
            logger.error(f"Error creating call log async: {str(e)}")
            return None

    async def get_active_calls_count(self):
        """
        Get count of currently active calls
        """
        return len(self.active_calls)

    async def get_call_details(self, channel_id):
        """
        Get details of a specific active call
        """
        return self.active_calls.get(channel_id)

    async def get_all_active_calls(self):
        """
        Get all active calls
        """
        return dict(self.active_calls)

    def stop_handler(self):
        """
        Stop the WebSocket handler gracefully
        """
        logger.info("Stopping ARI WebSocket handler...")
        # Additional cleanup can be added here if needed
        self.active_calls.clear()

    async def force_cleanup_old_calls(self, max_age_minutes=30):
        """
        Clean up calls that have been active too long (probably orphaned)
        """
        try:
            current_time = timezone.now()
            orphaned_calls = []
            
            for channel_id, call_data in self.active_calls.items():
                start_time = call_data.get('start_time')
                if start_time:
                    age_minutes = (current_time - start_time).total_seconds() / 60
                    if age_minutes > max_age_minutes:
                        orphaned_calls.append(channel_id)
            
            # Remove orphaned calls
            for channel_id in orphaned_calls:
                logger.warning(f"Removing orphaned call: {channel_id}")
                del self.active_calls[channel_id]
                
            if orphaned_calls:
                logger.info(f"Cleaned up {len(orphaned_calls)} orphaned calls")
                
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    async def log_system_stats(self):
        """
        Log system statistics periodically
        """
        try:
            active_count = len(self.active_calls)
            logger.info(f"System stats - Active calls: {active_count}")
            
            if active_count > 0:
                for channel_id, call_data in list(self.active_calls.items())[:5]:  # Log first 5
                    caller = call_data.get('caller_extension', 'Unknown')
                    callee = call_data.get('callee_extension', 'Unknown')
                    status = call_data.get('status', 'Unknown')
                    logger.info(f"  Active call: {caller} -> {callee} [{status}]")
                    
        except Exception as e:
            logger.error(f"Error logging stats: {str(e)}")
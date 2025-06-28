import requests
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class ARIClient:
    """
    Asterisk REST Interface (ARI) Client
    Handles HTTP requests to Asterisk ARI for extension management
    """
    
    def __init__(self):
        self.base_url = getattr(settings, 'ASTERISK_ARI_URL', 'http://localhost:8088/ari')
        self.username = getattr(settings, 'ASTERISK_ARI_USERNAME', 'ari_user')
        self.password = getattr(settings, 'ASTERISK_ARI_PASSWORD', 'ari_password')
        self.app_name = getattr(settings, 'ASTERISK_ARI_APP', 'django_calls')
        
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def create_extension(self, extension_username, extension_password):
        """
        Create SIP extension in Asterisk
        This would typically involve updating pjsip.conf or using realtime configuration
        For now, we'll simulate the creation and log it
        """
        try:
            # In a real implementation, you might:
            # 1. Update Asterisk configuration files
            # 2. Use Asterisk Manager Interface (AMI)
            # 3. Use database realtime configuration
            
            logger.info(f"Creating extension {extension_username} in Asterisk")
            
            # For demonstration, we'll assume the extension creation is successful
            # You would implement the actual Asterisk configuration update here
            
            # Example of what you might do:
            # - Update pjsip_endpoints table in database
            # - Reload Asterisk configuration
            # - Verify extension is registered
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create extension {extension_username}: {str(e)}")
            return False

    def delete_extension(self, extension_username):
        """
        Delete SIP extension from Asterisk
        """
        try:
            logger.info(f"Deleting extension {extension_username} from Asterisk")
            
            # Implementation would remove extension from Asterisk configuration
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete extension {extension_username}: {str(e)}")
            return False

    def check_extension_status(self, extension_username):
        """
        Check if extension is registered in Asterisk
        """
        try:
            # Check endpoint status via ARI
            response = self.session.get(f"{self.base_url}/endpoints/PJSIP/{extension_username}")
            
            if response.status_code == 200:
                endpoint_data = response.json()
                # Check if endpoint is online/registered
                return endpoint_data.get('state') == 'online'
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to check extension status for {extension_username}: {str(e)}")
            return False

    def get_active_calls(self):
        """
        Get list of active calls from Asterisk
        """
        try:
            response = self.session.get(f"{self.base_url}/channels")
            
            if response.status_code == 200:
                return response.json()
            
            return []
            
        except Exception as e:
            logger.error(f"Failed to get active calls: {str(e)}")
            return []

    def hangup_call(self, channel_id):
        """
        Hangup a specific call
        """
        try:
            response = self.session.delete(f"{self.base_url}/channels/{channel_id}")
            return response.status_code == 204
            
        except Exception as e:
            logger.error(f"Failed to hangup call {channel_id}: {str(e)}")
            return False

    def get_channel_info(self, channel_id):
        """
        Get information about a specific channel
        """
        try:
            response = self.session.get(f"{self.base_url}/channels/{channel_id}")
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get channel info for {channel_id}: {str(e)}")
            return None

    def start_recording(self, channel_id, recording_name):
        """
        Start recording a call
        """
        try:
            data = {
                'name': recording_name,
                'format': 'wav',
                'maxDurationSeconds': 3600,  # 1 hour max
                'terminateOn': 'none'
            }
            
            response = self.session.post(
                f"{self.base_url}/channels/{channel_id}/record",
                json=data
            )
            
            return response.status_code == 201
            
        except Exception as e:
            logger.error(f"Failed to start recording for {channel_id}: {str(e)}")
            return False

    def stop_recording(self, recording_name):
        """
        Stop a recording
        """
        try:
            response = self.session.delete(f"{self.base_url}/recordings/live/{recording_name}")
            return response.status_code == 204
            
        except Exception as e:
            logger.error(f"Failed to stop recording {recording_name}: {str(e)}")
            return False
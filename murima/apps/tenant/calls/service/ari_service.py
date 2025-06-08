# asterisk_app/services/ari_service.py
import asyncio
import websockets
import json
import aiohttp
import logging
from django.conf import settings
from typing import Tuple, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class AsteriskARIService:
    """
    Service to handle Asterisk ARI communication without external libraries.
    Uses direct WebSocket and HTTP connections.
    """
    
    def __init__(self):
        # Configuration - should be in Django settings
        self.ari_host = getattr(settings, 'ASTERISK_ARI_HOST', '18.177.175.202')
        self.ari_port = getattr(settings, 'ASTERISK_ARI_PORT', 8088)
        self.ari_username = getattr(settings, 'ASTERISK_ARI_USERNAME', 'djangoari')
        self.ari_password = getattr(settings, 'ASTERISK_ARI_PASSWORD', '2001')
        
        self.base_url = f"http://{self.ari_host}:{self.ari_port}/ari"
        self.websocket_url = f"ws://{self.ari_host}:{self.ari_port}/ari/events"
    
    async def _make_ari_request(self, method: str, endpoint: str, data: dict = None) -> Tuple[bool, Optional[dict]]:
        """
        Make HTTP request to ARI REST API
        """
        url = urljoin(self.base_url, endpoint)
        auth = aiohttp.BasicAuth(self.ari_username, self.ari_password)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=method,
                    url=url,
                    auth=auth,
                    json=data,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    
                    if response.status in [200, 201, 204]:
                        try:
                            result = await response.json()
                            return True, result
                        except:
                            return True, None
                    else:
                        error_text = await response.text()
                        logger.error(f"ARI request failed: {response.status} - {error_text}")
                        return False, {"error": error_text, "status": response.status}
        
        except Exception as e:
            logger.error(f"ARI request exception: {str(e)}")
            return False, {"error": str(e)}
    
    async def _connect_websocket(self) -> Optional[websockets.WebSocketServerProtocol]:
        """
        Connect to ARI WebSocket for real-time events
        """
        try:
            # WebSocket URL with authentication
            ws_url = f"{self.websocket_url}?api_key={self.ari_username}:{self.ari_password}&app=django_asterisk"
            
            websocket = await websockets.connect(
                ws_url,
                extra_headers={
                    "Authorization": f"Basic {self.ari_username}:{self.ari_password}"
                }
            )
            
            logger.info("Connected to Asterisk ARI WebSocket")
            return websocket
        
        except Exception as e:
            logger.error(f"Failed to connect to ARI WebSocket: {str(e)}")
            return None
    
    def create_extension(self, extension) -> Tuple[bool, Optional[str]]:
        """
        Create extension in Asterisk.
        This is a synchronous wrapper for the async method.
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self._create_extension_async(extension))
        except Exception as e:
            logger.error(f"Error in create_extension: {str(e)}")
            return False, str(e)
        finally:
            loop.close()
    
    async def _create_extension_async(self, extension) -> Tuple[bool, Optional[str]]:
        """
        Async method to create extension in Asterisk
        """
        try:
            # Step 1: Create SIP endpoint
            endpoint_data = {
                "name": extension.username,
                "auth": extension.username,
                "aors": extension.username,
                "context": f"tenant_{extension.tenant.id}",  # Tenant-specific context
            }
            
            success, result = await self._make_ari_request(
                "POST", 
                f"/endpoints/SIP/{extension.username}",
                endpoint_data
            )
            
            if not success:
                return False, f"Failed to create SIP endpoint: {result}"
            
            # Step 2: Create authentication
            auth_data = {
                "username": extension.username,
                "password": extension.password,
                "auth_type": "userpass"
            }
            
            success, result = await self._make_ari_request(
                "POST",
                f"/endpoints/SIP/{extension.username}/auth",
                auth_data
            )
            
            if not success:
                return False, f"Failed to create authentication: {result}"
            
            # Step 3: Create AOR (Address of Record)
            aor_data = {
                "contact": f"sip:{extension.username}@{extension.tenant.domain}",  # Adjust as needed
                "max_contacts": 1
            }
            
            success, result = await self._make_ari_request(
                "POST",
                f"/endpoints/SIP/{extension.username}/aor",
                aor_data
            )
            
            if not success:
                return False, f"Failed to create AOR: {result}"
            
            # Step 4: Add to dialplan (if needed via ARI)
            # Note: This might need to be done via configuration files
            # depending on your Asterisk setup
            
            logger.info(f"Successfully created Asterisk extension {extension.extension_number}")
            return True, None
        
        except Exception as e:
            error_msg = f"Exception creating extension: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def remove_extension(self, extension) -> Tuple[bool, Optional[str]]:
        """
        Remove extension from Asterisk
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self._remove_extension_async(extension))
        except Exception as e:
            logger.error(f"Error in remove_extension: {str(e)}")
            return False, str(e)
        finally:
            loop.close()
    
    async def _remove_extension_async(self, extension) -> Tuple[bool, Optional[str]]:
        """
        Async method to remove extension from Asterisk
        """
        try:
            # Remove SIP endpoint (this should cascade to auth and aor)
            success, result = await self._make_ari_request(
                "DELETE",
                f"/endpoints/SIP/{extension.username}"
            )
            
            if not success:
                return False, f"Failed to remove SIP endpoint: {result}"
            
            logger.info(f"Successfully removed Asterisk extension {extension.extension_number}")
            return True, None
        
        except Exception as e:
            error_msg = f"Exception removing extension: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def deactivate_extension(self, extension) -> Tuple[bool, Optional[str]]:
        """
        Deactivate extension (disable without deleting)
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self._deactivate_extension_async(extension))
        except Exception as e:
            logger.error(f"Error in deactivate_extension: {str(e)}")
            return False, str(e)
        finally:
            loop.close()
    
    async def _deactivate_extension_async(self, extension) -> Tuple[bool, Optional[str]]:
        """
        Async method to deactivate extension
        """
        try:
            # Update endpoint to disabled state
            endpoint_data = {
                "enabled": False
            }
            
            success, result = await self._make_ari_request(
                "PUT",
                f"/endpoints/SIP/{extension.username}",
                endpoint_data
            )
            
            if not success:
                return False, f"Failed to deactivate endpoint: {result}"
            
            logger.info(f"Successfully deactivated Asterisk extension {extension.extension_number}")
            return True, None
        
        except Exception as e:
            error_msg = f"Exception deactivating extension: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    async def get_extension_status(self, username: str) -> Tuple[bool, Optional[dict]]:
        """
        Get extension status from Asterisk
        """
        return await self._make_ari_request("GET", f"/endpoints/SIP/{username}")
    
    async def listen_to_events(self, callback=None):
        """
        Listen to Asterisk events via WebSocket
        """
        websocket = await self._connect_websocket()
        if not websocket:
            return
        
        try:
            async for message in websocket:
                try:
                    event = json.loads(message)
                    logger.info(f"Received ARI event: {event.get('type')}")
                    
                    if callback:
                        await callback(event)
                    
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse ARI event: {message}")
        
        except websockets.exceptions.ConnectionClosed:
            logger.warning("ARI WebSocket connection closed")
        except Exception as e:
            logger.error(f"Error in WebSocket listener: {str(e)}")
        finally:
            await websocket.close()
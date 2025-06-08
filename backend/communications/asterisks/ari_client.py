import websocket
import requests
import json
import time
import logging
import threading
from queue import Queue
from urllib.parse import quote

logger = logging.getLogger(__name__)

class ARIClient:
    def __init__(self, host='54.238.49.155', port=8088, username='asterisk',
                 password='asteriskpass', app_name='asterisk'):
        self.ws_url = f"wss://{host}:{port}/ari/events?api_key={username}:{password}&app={app_name}"
        self.base_url = f"http://{host}:{port}/ari"
        self.auth = (username, password)
        self.event_queue = Queue()
        self.ws = None
        self.active = True
        self.app_name = app_name
        self._initialize_logging()
        self.connected = False
        self.reconnect_delay = 5
    def _initialize_logging(self):
        """Configure logging settings"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('ari_client.log')
            ]
        )

    def start(self):
        """Start the ARI client components"""
        logger.info("Starting ARI Client")
        
        # Start WebSocket listener thread
        ws_thread = threading.Thread(
            target=self.start_websocket_listener,
            daemon=True,
            name="ARI-WebSocket-Thread"
        )
        ws_thread.start()
        
        # Start event processor thread
        processor_thread = threading.Thread(
            target=self.process_events,
            daemon=True,
            name="ARI-EventProcessor-Thread"
        )
        processor_thread.start()

    def start_websocket_listener(self):
        """Initialize and maintain WebSocket connection"""
        websocket.enableTrace(True)  # Keep True for debugging
        
        def on_message(ws, message):
            try:
                event = json.loads(message)
                logger.debug(f"Received event: {event.get('type')}")
                self.event_queue.put(event)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")

        def on_error(ws, error):
            logger.error(f"WebSocket error: {error}")
            self.connected = False

        def on_close(ws, close_status_code, close_msg):
            logger.warning(f"WebSocket closed ({close_status_code}): {close_msg}")
            self.connected = False
            if self.active:
                time.sleep(self.reconnect_delay)
                self._connect_websocket(on_message, on_error, on_close, on_open)

        def on_open(ws):
            logger.info("WebSocket connected, subscribing to events")
            self.connected = True


        self._connect_websocket(on_message, on_error, on_close, on_open)

    def _connect_websocket(self, on_message, on_error, on_close, on_open):
        """Handle WebSocket connection with retry logic"""
        while self.active:
            try:
                logger.info(f"Connecting to ARI WebSocket at {self.ws_url}")
                
                self.ws = websocket.WebSocketApp(
                    self.ws_url,
                    on_open=on_open,
                    on_message=on_message,
                    on_error=on_error,
                    on_close=on_close,
                    header=["Origin: http://localhost"]
                )
                
                self.ws.run_forever(
                    ping_interval=30,
                    ping_timeout=10,
                    sslopt={"cert_reqs": None},
                )
                
            except websocket.WebSocketConnectionClosedException:
                if self.active:
                    logger.warning("WebSocket connection closed, reconnecting...")
                    time.sleep(self.reconnect_delay)
            except Exception as e:
                logger.error(f"WebSocket error: {str(e)}")
                if self.active:
                    time.sleep(self.reconnect_delay)

  


    def process_events(self):
        """Process events from the queue"""
        logger.info("Event processor started")
        while self.active:
            try:
                event = self.event_queue.get(timeout=1)
                if event:
                    self.handle_event(event)
            except Exception as e:
                if self.active:
                    continue

    def handle_event(self, event):
        """Route incoming ARI events to appropriate handlers"""
        try:
            event_type = event.get('type')
            logger.debug(f"Handling {event_type} event")
            
            if event_type == 'StasisStart':
                self._handle_stasis_start(event)
            elif event_type == 'StasisEnd':
                self._handle_stasis_end(event)
            elif event_type == 'ChannelDestroyed':
                self._handle_channel_destroyed(event)
            elif event_type == 'PlaybackFinished':
                self._handle_playback_finished(event)
            # Add more event handlers as needed
                
        except Exception as e:
            logger.error(f"Error handling {event_type} event: {str(e)}")
            logger.debug(f"Event content: {json.dumps(event, indent=2)}")

    def _handle_stasis_start(self, event):
        """Handle StasisStart events"""
        channel_id = event['channel']['id']
        logger.info(f"Channel entered Stasis: {channel_id}")
        
        try:
            # Answer the channel
            self._ari_request(
                'post',
                f"channels/{channel_id}/answer",
                timeout=3
            )
            
            # Play greeting
            self._ari_request(
                'post',
                f"channels/{channel_id}/play",
                json={"media": "sound:hello-world"},
                timeout=3
            )
            
            # Schedule hangup
            threading.Timer(5.0, self._hangup_channel, args=[channel_id]).start()
            
        except Exception as e:
            logger.error(f"Error handling StasisStart: {str(e)}")

    def _handle_stasis_end(self, event):
        """Handle StasisEnd events"""
        channel_id = event['channel']['id']
        logger.info(f"Channel left Stasis: {channel_id}")

    def _handle_channel_destroyed(self, event):
        """Handle ChannelDestroyed events"""
        channel_id = event['channel']['id']
        logger.info(f"Channel destroyed: {channel_id}")

    def _handle_playback_finished(self, event):
        """Handle PlaybackFinished events"""
        logger.info(f"Playback finished: {event.get('playback', {}).get('id')}")

    def _hangup_channel(self, channel_id):
        """Hang up a channel"""
        try:
            self._ari_request(
                'delete',
                f"channels/{channel_id}",
                timeout=3
            )
        except Exception as e:
            logger.error(f"Error hanging up channel {channel_id}: {str(e)}")

    def _ari_request(self, method, endpoint, **kwargs):
        """Helper method for ARI requests"""
        methods = {
            'get': requests.get,
            'post': requests.post,
            'delete': requests.delete,
            'put': requests.put
        }
        
        url = f"{self.base_url}/{endpoint}"
        logger.debug(f"Making {method.upper()} request to {url}")
        
        try:
            response = methods[method](
                url,
                auth=self.auth,
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"ARI request failed: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.status_code} - {e.response.text}")
            raise

    def stop(self):
        """Gracefully shutdown the ARI client"""
        logger.info("Shutting down ARI client")
        self.active = False
        
        if self.ws:
            self.ws.close()
        
        # Clear the event queue
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except:
                pass
                
        logger.info("ARI client shutdown complete")


# Example usage
if __name__ == "__main__":
    client = ARIClient()
    client.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.stop()
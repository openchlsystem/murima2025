from django.apps import AppConfig
from .asterisks.ari_client import ARIClient

class CommunicationsConfig(AppConfig):
    name = 'communications'

    def ready(self):
        if not hasattr(self, 'ari_started'):
            self.ari_started = True
            self.start_ari()

    def start_ari(self):
        import threading
        ari = ARIClient()
        
        # Start WebSocket thread
        ws_thread = threading.Thread(
            target=ari.start_websocket_listener,
            daemon=True
        )
        ws_thread.start()
        
        # Start event processing thread
        event_thread = threading.Thread(
            target=ari.process_events,
            daemon=True
        )
        event_thread.start()
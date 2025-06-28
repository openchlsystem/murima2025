import asyncio
import signal
import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from calls.services.websocket_handler import ARIWebSocketHandler
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start the ARI WebSocket listener for call events'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reconnect-delay',
            type=int,
            default=5,
            help='Delay in seconds before reconnecting after connection loss'
        )

    def handle(self, *args, **options):
        """
        Main command handler
        """
        self.stdout.write(
            self.style.SUCCESS('Starting ARI WebSocket listener...')
        )

        # Create WebSocket handler
        self.ws_handler = ARIWebSocketHandler()
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        try:
            # Start the async event loop
            asyncio.run(self.run_listener())
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('Received interrupt signal, shutting down...')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error in ARI listener: {str(e)}')
            )
            sys.exit(1)

    async def run_listener(self):
        """
        Run the WebSocket listener
        """
        try:
            await self.ws_handler.connect_and_listen()
        except Exception as e:
            logger.error(f"Error in WebSocket listener: {str(e)}")
            raise

    def signal_handler(self, signum, frame):
        """
        Handle shutdown signals gracefully
        """
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        
        # Stop the WebSocket handler
        if hasattr(self, 'ws_handler'):
            self.ws_handler.stop_handler()
        
        self.stdout.write(
            self.style.SUCCESS('ARI WebSocket listener stopped')
        )
        sys.exit(0)
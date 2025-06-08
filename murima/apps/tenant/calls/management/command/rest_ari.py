# asterisk_app/management/commands/test_ari.py
import asyncio
from django.core.management.base import BaseCommand
from calls.services.ari_service import AsteriskARIService


class Command(BaseCommand):
    help = 'Test Asterisk ARI connection'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--test-websocket',
            action='store_true',
            help='Test WebSocket connection',
        )
    
    def handle(self, *args, **options):
        self.stdout.write('Testing Asterisk ARI connection...')
        
        ari_service = AsteriskARIService()
        
        # Test HTTP connection
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Test basic API call
            success, result = loop.run_until_complete(
                ari_service._make_ari_request("GET", "/asterisk/info")
            )
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✓ ARI HTTP connection successful')
                )
                self.stdout.write(f'Asterisk version: {result.get("build", {}).get("version", "Unknown")}')
            else:
                self.stdout.write(
                    self.style.ERROR('✗ ARI HTTP connection failed')
                )
                self.stdout.write(f'Error: {result}')
            
            # Test WebSocket connection if requested
            if options['test_websocket']:
                self.stdout.write('Testing WebSocket connection...')
                
                async def test_ws():
                    websocket = await ari_service._connect_websocket()
                    if websocket:
                        self.stdout.write(
                            self.style.SUCCESS('✓ ARI WebSocket connection successful')
                        )
                        await websocket.close()
                        return True
                    else:
                        self.stdout.write(
                            self.style.ERROR('✗ ARI WebSocket connection failed')
                        )
                        return False
                
                loop.run_until_complete(test_ws())
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Connection test failed: {str(e)}')
            )
        finally:
            loop.close()
        
        self.stdout.write('Test completed.')
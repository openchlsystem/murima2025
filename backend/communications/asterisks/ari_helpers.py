
def handle_ari_event(event):
    if event['type'] == 'StasisStart':
        print(f"Call entered ARI: {event['channel']['id']}")
    elif event['type'] == 'ChannelDestroyed':
        print(f"Call ended: {event['channel']['id']}")
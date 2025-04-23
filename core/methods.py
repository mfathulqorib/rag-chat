from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_notification(notification_type, content):
    channel = get_channel_layer()
    async_to_sync(channel.group_send)('notifications', {
        'type': 'send_notification',
        'message': {
            'content': content,
            'type': notification_type
        },
    })

def send_chat_message(message, session_id):
    channel = get_channel_layer()
    async_to_sync(channel.group_send)(
        f"chat_{session_id}", 
        {
            'type': 'send_message',
            'message':message
        }
    )
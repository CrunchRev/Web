"""
2024, Written by the CrunchRev Authors

Module description: controls webhooks
"""

import requests
import logging

webhook_logger = logging.getLogger('CrunchRev Webhooks Logs')
webhook_logger.setLevel(logging.INFO)

def send_arbiter_startup_webhook(placeId, client):
    webhook_url = "https://discord.com/api/webhooks/1271089751297884271/WwAXdJVNPAd7XVpRKYgphQSUr7rxbQ3v9ScQjQwedrVFRwZ-zF7OLEtuEnqy-32cKoOC"

    embed = {
        "title": "Arbiter Startup Notification",
        "description": f"The arbiter service has started successfully for placeId: {placeId} and client: {client}.",
        "color": 0x00ff00,
        "fields": [
            {
                "name": "Place ID",
                "value": str(placeId),
                "inline": False
            },
            {
                "name": "Client",
                "value": client,
                "inline": True
            },
            {
                "name": "Status",
                "value": "Running",
                "inline": True
            }
        ],
        "footer": {
            "text": "Service Monitor",
        }
    }

    data = {
        "username": "Arbiter Bot",
        "content": "Service Startup Notification:",
        "embeds": [embed]
    }

    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        webhook_logger.info("Message sent successfully")
    else:
        webhook_logger.error(f"Failed to send message: {response.status_code}")
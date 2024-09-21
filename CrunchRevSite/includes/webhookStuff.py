"""
2024, Written by the CrunchRev Authors

Module description: controls webhooks
"""

import requests
import logging
import json
import xml.etree.ElementTree as ET # we will parse that shit!

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

webhook_logger = logging.getLogger('CrunchRev Webhooks Logs')
webhook_logger.setLevel(logging.INFO)

def send_webhook_signup(username, inv, user_id):
    webhook_url = "https://discord.com/api/webhooks/1255824113440657408/VwU0AElxaltgwFR_KDVJl3EDs8BFljgV1iK1MOuVAoGDslWzvWVVgl7aRLDuB63P86gU"
    content = "New User!"
    
    embed = {
        "title": "New User Registered",
        "fields": [
            {"name": "Username", "value": username, "inline": True},
            {"name": "Invite Key Used", "value": inv, "inline": True},
            {"name": "User ID", "value": user_id, "inline": True},
        ],
        "color": 0x00ff00  # green
    }

    data = {
        "content": content,
        "embeds": [embed]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            webhook_logger.info("Webhook sent successfully!")
        else:
            webhook_logger.error(f"Failed to send webhook. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        webhook_logger.error(f"Error sending webhook: {e}")

def send_arbiter_startup_webhook(placeId, client, servah):
    webhook_url = "https://discord.com/api/webhooks/1271089751297884271/WwAXdJVNPAd7XVpRKYgphQSUr7rxbQ3v9ScQjQwedrVFRwZ-zF7OLEtuEnqy-32cKoOC"

    embed = {
        "title": "RCCService Startup Notification",
        "description": f"The RCCService has started successfully for placeId: {placeId} and client: {client} on the server IP: {servah}.",
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
                "name": "Server IP",
                "value": servah,
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

def sendReportAbuse(xml_data):
    webhook_url = "https://discord.com/api/webhooks/1278739622406389812/_Q7spNKO3-kTn8YUXmBezItV_QgwGdQfQDL-4R-dw2dV35pF-yr8WNAgUwsVlgBY_QKB"
    
    root = ET.fromstring(xml_data)
    userID = root.attrib.get("userID")
    placeID = root.attrib.get("placeID")
    gameJobID = root.attrib.get("gameJobID")
    userSystemAddress = root.attrib.get("userSystemAddress", "N/A")
    userAgent = root.findtext("userAgent", "N/A")
    comment = root.findtext("comment", "No comment provided")
    
    messages = root.find("messages")
    message_details = "\n".join([f"User {msg.attrib['userID']} (GUID: {msg.attrib['guid']}): {msg.text}" for msg in messages[-5:]])

    embed = {
        "title": "Abuse Report Submitted",
        "description": "Details from the abuse report",
        "fields": [
            {"name": "User ID", "value": userID, "inline": True},
            {"name": "Place ID", "value": placeID, "inline": True},
            {"name": "Game Job ID", "value": gameJobID, "inline": False},
            {"name": "User System Address", "value": userSystemAddress, "inline": False},
            {"name": "User Agent", "value": userAgent, "inline": False},
            {"name": "Comment", "value": comment, "inline": False},
            {"name": "Messages", "value": message_details, "inline": False}
        ],
        "color": 15158332
    }
    
    data = {
        "embeds": [embed]
    }

    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        webhook_logger.info("Message sent successfully")
    else:
        webhook_logger.error(f"Failed to send message: {response.status_code}")

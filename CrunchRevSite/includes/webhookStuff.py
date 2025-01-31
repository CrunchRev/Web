"""
2024 - 2025, Written by the CrunchRev Authors

Module description: controls webhooks
"""

import requests
import logging
import json
import xml.etree.ElementTree as ET # we will parse that shit!
from settings import settings

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

webhook_logger = logging.getLogger('CrunchRev Webhooks Logs')
webhook_logger.setLevel(logging.INFO)

class Webhooks:
    def __init__(self) -> None:
        pass

    def send_webhook_signup(self, username, inv, user_id):
        webhook_url = "https://discordapp.com/api/webhooks/1327718765160300655/BHJLCvl3CQHO3_rQDyKPjGZExWOoZS6dY83mVhar4QdMR6MZiq1aRxS065pqnen0Y0da"
        content = "New User!"
        
        embed = {
            "title": "New User Registered",
            "fields": [
                {"name": "Username", "value": username, "inline": True},
                {"name": "Invite Key Used", "value": inv, "inline": True},
                {"name": "User ID", "value": user_id, "inline": True},
            ],
            "color": 0x00ff00
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

            if response.status_code in (200, 204):
                webhook_logger.info("Webhook sent successfully!")
            else:
                webhook_logger.error(f"Failed to send webhook. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            webhook_logger.error(f"Error sending webhook: {e}")

    def send_arbiter_startup_webhook(self, placeId, client, servah, jobId, port, status):
        webhook_url = "https://discordapp.com/api/webhooks/1327719377260515460/1el1osXDYSOT-tYeavEqD_NqW4-Tk7JGeUPOtI9dpfMfPp6PHLMbx2xcNUFw22TJd-eA"

        embed = {
            "title": "RCCService Notification",
            "description": f"The RCCService has changed it's status successfully for placeId: `{placeId}` and client: `{client}` with the job ID of `{jobId}` on the server IP: `{servah}`, and port: `{port}`.",
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
                    "name": "Network Port",
                    "value": port,
                    "inline": True
                },
                {
                    "name": "Job ID",
                    "value": jobId,
                    "inline": True
                },
                {
                    "name": "Status",
                    "value": status,
                    "inline": True
                }
            ],
            "footer": {
                "text": "Service Monitor",
            }
        }

        data = {
            "username": "Arbiter Bot",
            "content": "Service Notification:",
            "embeds": [embed]
        }

        response = requests.post(webhook_url, json=data)

        if response.status_code in (200, 204):
            webhook_logger.info("Message sent successfully")
        else:
            webhook_logger.error(f"Failed to send message: {response.status_code}")

    def sendReportAbuse(self, xml_data):
        webhook_url = "https://discordapp.com/api/webhooks/1327719958192455762/-InQXdSEhLYy7jDEp_LpiZWNwHo5Wxgh2hSGHJ_nxg5eo5vtT0S2Ov9xFnHa8iXkoRyQ"
        
        root = ET.fromstring(xml_data)
        userID = root.attrib.get("userID")
        placeID = root.attrib.get("placeID")
        gameJobID = root.attrib.get("gameJobID")
        userSystemAddress = root.attrib.get("userSystemAddress", "N/A")
        userAgent = root.findtext("userAgent", "N/A")
        comment = root.findtext("comment", "No comment provided")
        
        messages = root.find("messages")
        message_details = "\n".join([f"User {msg.attrib['userID']} (GUID: {msg.attrib['guid']}): {msg.text}" for msg in messages])

        report_content = f"""Abuse Report:
User ID: {userID}
Place ID: {placeID}
Game Job ID: {gameJobID}
User System Address: {userSystemAddress}
User Agent: {userAgent}
Comment: 

{comment}
    
Messages:

{message_details}"""

        files = {
            'file': ('abuse_report.txt', report_content)
        }

        response = requests.post(webhook_url, files=files)

        if response.status_code in (200, 204):
            webhook_logger.info("Report sent successfully")
        else:
            webhook_logger.error(f"Failed to send report: {response.status_code}")

    def sendSysStats(self, placeID, userID, message, resolution):
        webhook_url = "https://discordapp.com/api/webhooks/1327716225945571369/AUzSLP9Fq2p3XulTfJ1N4DYaflo1URZRbMpq0PHGZCfMBYCZ3dMVGyATZqD6loMtEWT8"

        sysMsgs = settings["sysStatsMessages"]

        fullMessage = sysMsgs[message] if message in sysMsgs else "No explanation found"

        embed = {
            "title": "SysStats (System Statistics) Report",
            "color": 0x00ff00,
            "fields": [
                {
                    "name": "Place ID",
                    "value": f"`{placeID}`",
                    "inline": True
                },
                {
                    "name": "User ID",
                    "value": f"`{userID}`",
                    "inline": True
                },
                {
                    "name": "Message",
                    "value": f"`{message} ({fullMessage})`",
                    "inline": False
                },
                {
                    "name": "Resolution",
                    "value": f"`{resolution}`",
                    "inline": True
                }
            ]
        }

        data = {
            "username": "SysStats Reporter Webhook",
            "embeds": [embed]
        }

        response = requests.post(webhook_url, json=data)

        if response.status_code in (200, 204):
            webhook_logger.info("Message sent successfully")
        else:
            webhook_logger.error(f"Failed to send message: {response.status_code}")
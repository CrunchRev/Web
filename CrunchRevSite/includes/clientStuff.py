"""
2024, Written by the CrunchRev Authors

Module description: controls rbxsig and tickets
"""

from OpenSSL import crypto
from datetime import datetime
import base64
import random
import logging

from includes.webhookStuff import *

Webhooks = Webhooks()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sm_logger = logging.getLogger('CrunchRev Server Management Logs')
sm_logger.setLevel(logging.INFO)

class Signer:
    def __init__(self, PK1024Path, PK2048Path):
        self.PK1024Path = PK1024Path
        self.PK2048Path = PK2048Path
        return None

    def sign_v1(self, data):
        with open(self.PK1024Path, "r") as key_file:
            private_key = key_file.read()

        key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key)
        signer = crypto.sign(key, data, "sha1")
        signature = base64.b64encode(signer).decode("utf-8")
        return f"--rbxsig%{signature}%{data}"
    
    def sign_v2(self, data):
        with open(self.PK2048Path, "r") as key_file:
            private_key = key_file.read()

        key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key)
        signer = crypto.sign(key, data, "sha1")
        signature = base64.b64encode(signer).decode("utf-8")
        return f"--rbxsig2%{signature}%{data}"

class Tickets:
    def __init__(self, PK1024Path, PK2048Path):
        self.PK1024Path = PK1024Path
        self.PK2048Path = PK2048Path
        return None

    def generate_client_ticket_v1(self, user_id, username, character_app, job_id):
        with open(self.PK1024Path, "r") as key_file:
            private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())

        curr_date = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

        ticket = f"{user_id}\n{job_id}\n{curr_date}"

        sig = crypto.sign(private_key, ticket.encode(), "sha1")
        sig = base64.b64encode(sig).decode()

        ticket2 = f"{user_id}\n{username}\n{character_app}\n{job_id}\n{curr_date}"

        sig2 = crypto.sign(private_key, ticket2.encode(), "sha1")
        sig2 = base64.b64encode(sig2).decode()

        final = f"{curr_date};{sig2};{sig}"

        return final

    def generate_client_ticket_v2(self, user_id, username, job_id):
        with open(self.PK2048Path, "r") as key_file:
            private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())

        curr_date = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

        ticket = f"{user_id}\n{job_id}\n{curr_date}"

        sig = crypto.sign(private_key, ticket.encode(), "sha1")
        sig = base64.b64encode(sig).decode()

        ticket2 = f"{user_id}\n{username}\n{user_id}\n{job_id}\n{curr_date}"

        sig2 = crypto.sign(private_key, ticket2.encode(), "sha1")
        sig2 = base64.b64encode(sig2).decode()

        final = f"{curr_date};{sig2};{sig};2"

        return final

    def generate_client_ticket_v4(self, user_id, username, job_id, charapp):
        with open(self.PK2048Path, "r") as key_file:
            private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())

        curr_date = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')

        ticket = f"{curr_date}\n{job_id}\n{user_id}\n{user_id}\n0\n1000\nf\n{len(username)}\n{username}\n4\nNone\n0\n\n0\n\n{len(username)}\n{username}"

        logging.info(f"Ticket 1: {ticket}")

        sig = crypto.sign(private_key, ticket.encode(), "sha1")
        sig = base64.b64encode(sig).decode()

        ticket2 = f"{user_id}\n{username}\n{charapp}\n{job_id}\n{curr_date}"

        logging.info(f"Ticket 2: {ticket2}")

        sig2 = crypto.sign(private_key, ticket2.encode(), "sha1")
        sig2 = base64.b64encode(sig2).decode()

        final = f"{curr_date};{sig2};{sig};4"

        logging.info(f"Final Ticket: {final}")

        return final

class Arbiter:
    def __init__(self, arbiterURLs, DBClass, GamesClass):
        self.arbiterURLs = arbiterURLs
        self.db = DBClass
        self.games = GamesClass
        return None

    def addJobDB(self, serverIP, networkPort, jobID, placeID, year, status):
        sqlQuery = """
        INSERT INTO `jobs_in_use` (`RCC_Version`, `place_id`, `jobId`, `network_port`, `server_address`, `status`) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        `status` = VALUES(`status`)
        """
        self.db.bulk_insert(sqlQuery, param_list=[(year, placeID, jobID, networkPort, serverIP, status)])

    def requestServer(self, year, placeID, maxPlayers, creatorId):
        arbiterURL = random.choice(list(self.arbiterURLs))
        place = self.games.fetchOne(placeID)

        if place["info"] is None:
            return {
                "success": False,
                "status": 4,
                "message": "Game failed to start"
            }

        sql = "SELECT * FROM `jobs_in_use` WHERE `place_id` = %s AND `players` < %s AND `status` = 2 ORDER BY RAND() LIMIT 1;"
        execution1 = self.db.execute_securely(sql, params=(placeID, place["info"][2]))

        if execution1 is None:
            # no servers avaliable, request a new one.

            sql2 = "SELECT jobId FROM `jobs_in_use` WHERE `place_id` = %s AND `status` = 0 OR `status` = 1" # idfk how to do that
            execution2 = self.db.execute_securely(sql2, params=(placeID))

            if execution2 is not None:
                try:
                    requestArbiter2 = requests.post(f"http://{arbiterURL}/arbiter/gameserver", json={"jobId": execution2[0], "apiKey": "ddec2ab4ae78dda0bb3497b134ae5c61"})
                except:
                    sm_logger.error(f"Failed to request server from {arbiterURL}")
                    return {
                        "success": True,
                        "status": 0,
                        "message": "",
                        "jobId": ""
                    }
                
                if not requestArbiter2.status_code == requests.codes.ok:
                    return {
                        "success": True,
                        "status": 1,
                        "message": "",
                        "jobId": ""
                    }
                
                try:
                    json2 = requestArbiter2.json()
                except:
                    return {
                        "success": True,
                        "status": 1,
                        "message": "",
                        "jobId": ""
                    }
                
                self.addJobDB(json2["ip"], json2["port"], json2["jobId"], placeID, year, json2["status"])

                Webhooks.send_arbiter_startup_webhook(placeID, year, json2["ip"], json2["jobId"], json2["port"], json2["status"])
            
                return {
                    "success": True,
                    "status": json2["status"],
                    "message": "",
                    "jobId": json2["jobId"]
                }

            try:
                requestArbiter = requests.post(f"http://{arbiterURL}/arbiter/gameserver", json={"clientYear": year, "placeId": placeID, "maxPlayers": maxPlayers, "creatorId": creatorId, "apiKey": "ddec2ab4ae78dda0bb3497b134ae5c61"})
            except:
                sm_logger.error(f"Failed to request server from {arbiterURL}")
                return {
                    "success": True,
                    "status": 0,
                    "message": "",
                    "jobId": ""
                }
            
            if not requestArbiter.status_code == requests.codes.ok:
                return {
                    "success": True,
                    "status": 0,
                    "message": "",
                    "jobId": ""
                }
            
            try:
                json = requestArbiter.json()
            except:
                return {
                    "success": True,
                    "status": 0,
                    "message": "",
                    "jobId": ""
                }
            
            self.addJobDB(json["ip"], json["port"], json["jobId"], placeID, year, json["status"])

            Webhooks.send_arbiter_startup_webhook(placeID, year, json["ip"], json["jobId"], json["port"], json["status"])
        
            return {
                "success": True,
                "status": json["status"],
                "message": "",
                "jobId": json["jobId"]
            }
        else:
            # server is avaliable, return it.
            return {
                "success": True,
                "status": 2,
                "message": "",
                "jobId": execution1[2]
            }

    def getInformationViaJobID(self, jobID):
        sql = "SELECT * FROM `jobs_in_use` WHERE `jobId` = %s"

        return self.db.execute_securely(sql, (jobID,)) or None
        
    def boomboomjobIds(self, placeId): # I am silly xD
        sql = "DELETE FROM `jobs_in_use` WHERE `place_id` = %s"
        self.db.execute_securely(sql, (placeId,))

    def boomboomjobId(self, jobId): # I am silly xD x2
        sql = "DELETE FROM `jobs_in_use` WHERE `jobId` = %s"
        self.db.execute_securely(sql, (jobId,))

    def getServerAddressUsingJobId(self, jobId):
        sql = "SELECT server_address FROM `jobs_in_use` WHERE `jobId` = %s"
        return self.db.execute_securely(sql, (jobId,))

    def shutdownPlaceIdServers(self, placeId):
        arbiterURLsList = list(self.arbiterURLs)
        results = []
        
        for url in arbiterURLsList:
            try:
                getRequest = requests.post(f"http://{url}/arbiter/gameserver/stop/placeAll", json={"placeId": placeId, "apiKey": "ddec2ab4ae78dda0bb3497b134ae5c61"}, timeout=3.5)
                results.append(getRequest.json())
            except:
                sm_logger.error(f"Failed to shutdown servers on {url}, skipping...")
                continue
        
        if results:
            self.boomboomjobIds(placeId)

            return {"success": True, "results": results}
        else:
            return {"success": False, "message": "Failed to shutdown servers"}

    def shutdownJobId(self, jobId):
        geti = self.getInformationViaJobID(jobId)
        url = geti[0] if len(geti) > 0 else None

        if url is None:
            return {"success": False, "message": "Failed to shutdown job id"}

        arbiterURL = f"{url}:7209"
        try:
            getRequest = requests.post(f"http://{arbiterURL}/arbiter/gameserver/stop", json={"jobId": jobId, "apiKey": "ddec2ab4ae78dda0bb3497b134ae5c61"}, timeout=3.5)
            self.boomboomjobId(jobId)
            return getRequest.json()
        except:
            sm_logger.error(f"Failed to shutdown servers on {arbiterURL}")

        return {"success": False, "message": "Failed to shutdown job id"}

    def updatePlayersOnJob(self, jobId, playersAmount):
        query = "UPDATE jobs_in_use SET players = %s WHERE jobId = %s"
        self.db.execute_securely(query, (playersAmount, jobId))

        return True

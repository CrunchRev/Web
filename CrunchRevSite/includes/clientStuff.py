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

        ticket = f"{user_id}\n{job_id}\n{datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}"

        sig = crypto.sign(private_key, ticket.encode(), "sha1")
        sig = base64.b64encode(sig).decode()

        ticket2 = f"{user_id}\n{username}\n{character_app}\n{job_id}\n{datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}"

        sig2 = crypto.sign(private_key, ticket2.encode(), "sha1")
        sig2 = base64.b64encode(sig2).decode()

        final = f"{datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')};{sig2};{sig}"

        return final

    def generate_client_ticket_v2(self, user_id, username, job_id):
        with open(self.PK2048Path, "r") as key_file:
            private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())

        ticket = f"{user_id}\n{job_id}\n{datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}"

        sig = crypto.sign(private_key, ticket.encode(), "sha1")
        sig = base64.b64encode(sig).decode()

        ticket2 = f"{user_id}\n{username}\n{user_id}\n{job_id}\n{datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}"

        sig2 = crypto.sign(private_key, ticket2.encode(), "sha1")
        sig2 = base64.b64encode(sig2).decode()

        final = f"{datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')};{sig2};{sig};2"

        return final

    def generate_client_ticket_v4(self, user_id, username, job_id, charapp):
        with open(self.PK2048Path, "r") as key_file:
            private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())

        ticket = f"{datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}\n{job_id}\n{user_id}\n{user_id}\n0\n1000\nf\n{len(username)}\n{username}\n4\nNone\n0\n\n0\n\n{len(username)}\n{username}"

        sig = crypto.sign(private_key, ticket.encode(), "sha1")
        sig = base64.b64encode(sig).decode()

        ticket2 = f"{user_id}\n{username}\n{charapp}\n{job_id}\n{datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}"

        sig2 = crypto.sign(private_key, ticket2.encode(), "sha1")
        sig2 = base64.b64encode(sig2).decode()

        final = f"{datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')};{sig2};{sig};4"

        return final

class Arbiter:
    def __init__(self, arbiterURLs, DBClass, GamesClass):
        self.arbiterURLs = arbiterURLs
        self.db = DBClass
        self.games = GamesClass
        return None

    def addJobDB(self, serverIP, networkPort, jobID, placeID, year):
        # pizdec
        sqlQuery = "INSERT INTO `jobs_in_use`(`RCC_Version`, `place_id`, `jobId`, `network_port`, `server_address`) VALUES ( %s, %s, %s, %s, %s )"
        self.db.execute_securely(sqlQuery, params=(year, placeID, jobID, networkPort, serverIP))

    def requestServer(self, year, placeID):
        arbiterURL = random.choice(list(self.arbiterURLs))
        place = self.games.fetchOne(placeID)

        if place["info"] is None:
            return {
                "success": False,
                "status": 4,
                "message": "Game failed to start"
            }

        sql = "SELECT * FROM `jobs_in_use` WHERE `place_id` = %s AND `players` < %s ORDER BY RAND() LIMIT 1;"
        execution1 = self.db.execute_securely(sql, params=(placeID, place["info"][2]))

        if execution1 is None:
            # no servers avaliable, request a new one.
            try:
                requestArbiter = requests.get(f"http://{arbiterURL}/internal/arbiter/startgameserver?year={year}&placeId={placeID}&accessKey=ddec2ab4ae78dda0bb3497b134ae5c61")
            except:
                sm_logger.error(f"Failed to request server from {arbiterURL}, retrying...")
                return self.requestServer(year, placeID)
            
            if not requestArbiter.status_code == requests.codes.ok:
                return {
                    "success": False,
                    "status": 4,
                    "message": "Game failed to start"
                }
            
            json = requestArbiter.json()

            if not "success" in json:
                return {
                    "success": False,
                    "status": 4,
                    "message": "Game failed to start"
                }

            if json["success"] == True:
                # success case, open job and return 1
                self.addJobDB(json["serverAddress"], json["networkPort"], json["jobId"], placeID, year)
                send_arbiter_startup_webhook(placeID, year, json["serverAddress"])
                return {
                    "success": True,
                    "status": 1,
                    "message": "",
                    "jobId": ""
                }
            else:
                # unsuccess D:
                return {
                    "success": False,
                    "status": 4,
                    "message": "Game failed to start"
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
                getRequest = requests.get(f"http://{url}/internal/gameserver/shutdownallservers?placeId={str(placeId)}&accessKey=ddec2ab4ae78dda0bb3497b134ae5c61")
                self.boomboomjobIds(placeId)
                results.append(getRequest.json())
            except:
                sm_logger.error(f"Failed to shutdown servers on {url}, skipping...")
                continue
        
        if results:
            return {"success": True, "results": results}
        else:
            return {"success": False, "message": "Failed to shutdown servers"}

    def shutdownJobId(self, jobId):
        arbiterURL = f"{self.getServerAddressUsingJobId(jobId)[0]}:7209"
        try:
            getRequest = requests.get(f"http://{arbiterURL}/internal/gameserver/shutdownjobid?jobId={str(jobId)}&accessKey=ddec2ab4ae78dda0bb3497b134ae5c61")
            self.boomboomjobId(jobId)
            return getRequest.json()
        except:
            sm_logger.error(f"Failed to shutdown servers on {arbiterURL}")

        return {"success": False, "message": "Failed to shutdown job id"}
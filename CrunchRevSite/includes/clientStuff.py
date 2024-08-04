"""
2024, Written by the CrunchRev Authors

Module description: controls rbxsig and tickets
"""

from __main__ import *

from OpenSSL import crypto
from datetime import datetime
import base64

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

    def generate_client_ticket_v2(self, userId, username, jobId):
        with open(self.PK2048Path, "r") as key_file:
            private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())

        current_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        
        ticket = f"{userId}\n{jobId}\n{current_time}"
        signature = crypto.sign(privatekey, ticket.encode('utf-8'), "sha1")
        sig = base64.b64encode(signature).decode('utf-8')

        ticket2 = f"{userId}\n{username}\n{userId}\n{jobId}\n{current_time}"
        signature2 = crypto.sign(privatekey, ticket2.encode('utf-8'), "sha1")
        sig2 = base64.b64encode(signature2).decode('utf-8')

        final = f"{current_time};{sig2};{sig};2"
        
        return final

class Arbiter:
    def __init__(self, arbiterURL, DBClass, GamesClass):
        self.arbiterURL = arbiterURL
        self.db = DBClass
        self.games = GamesClass
        return None

    def addJobDB(self, serverIP, networkPort, jobID, placeID, year):
        # pizdec
        sqlQuery = "INSERT INTO `jobs_in_use`(`RCC_Version`, `place_id`, `jobId`, `network_port`, `server_address`) VALUES ( %s, %s, %s, %s, %s )"
        self.db.execute_securely(sqlQuery, params=(year, placeID, jobID, networkPort, serverIP))

    def requestServer(self, year, placeID):
        place = self.games.fetchOne(placeID)

        if place["info"] is None:
            return {
                "success": False,
                "status": 4,
                "message": "Game failed to start"
            }

        sql = "SELECT * FROM `jobs_in_use` WHERE `place_id` = %s AND `players` < %s"
        execution1 = self.db.execute_securely(sql, params=(placeID, place["info"][2]), fetch_all=True)

        if len(execution1) < 1:
            # no servers avaliable, request a new one.
            try:
                requestArbiter = requests.get(f"http://{self.arbiterURL}/internal/arbiter/startgameserver?year={year}&placeId={placeID}")
            except:
                return {
                    "success": False,
                    "status": 4,
                    "message": "Game failed to start"
                }
            
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
                self.addJobDB(json["serverAdress"], json["networkPort"], json["jobId"], placeID, year)
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
                "jobId": execution1[0][2]
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

    def shutdownPlaceIdServers(self, placeId):
        getRequest = requests.get(f"http://{self.arbiterURL}/internal/gameserver/shutdownallservers?placeId={str(placeId)}")
        self.boomboomjobIds(placeId)
        return getRequest.json()

    def shutdownJobId(self, jobId):
        getRequest = requests.get(f"http://{self.arbiterURL}/internal/gameserver/shutdownjobid?jobId={str(jobId)}")
        self.boomboomjobId(jobId)
        return getRequest.json()
"""
2024, Written by the CrunchRev Authors

Main CrunchRev core code
"""

import logging
import traceback
import json
import uuid
import time
import os
from flask import *
import requests
from waitress import serve
from paste.translogger import TransLogger
from flask_bcrypt import Bcrypt
from functools import lru_cache
import xml.etree.ElementTree as ET
from io import BytesIO
import gzip
import random
import datetime
from flask_limiter import Limiter
import warnings
import threading

from settings import settings
from includes.clientStuff import *
from includes.chatStuff import *
from includes.databaseStuff import *
from includes.safeTokensStuff import *
from includes.webhookStuff import *

print(r"""
   ____                       _     ____             __        __   _         _ _       
  / ___|_ __ _   _ _ __   ___| |__ |  _ \ _____   __ \ \      / /__| |__  ___(_) |_ ___ 
 | |   | '__| | | | '_ \ / __| '_ \| |_) / _ \ \ / /  \ \ /\ / / _ \ '_ \/ __| | __/ _ \
 | |___| |  | |_| | | | | (__| | | |  _ <  __/\ V /    \ V  V /  __/ |_) \__ \ | ||  __/
  \____|_|   \__,_|_| |_|\___|_| |_|_| \_\___| \_/      \_/\_/ \___|_.__/|___/_|\__\___|
""")
print("Made by the CrunchRev Authors, 2024")
print("Do not leak this or this might give you a punishment.")
print("---------------------------------------------------------------------------------------------")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

internal_logger = logging.getLogger('CrunchRev Internal Logs')
internal_logger.setLevel(logging.INFO)

internal_logger.info("Setting up logging (1 / 2)...")

waitress_logger = logging.getLogger('waitress')
waitress_logger.setLevel(logging.INFO)

internal_logger.info("Setting up logging (2 / 2)...")

internal_logger.info("Connecting to remote MySQL server...")
try:
    Database = Database(settings["Database"])
    internal_logger.info("Successfully connected to the remote MySQL server.")
except Exception as e:
    internal_logger.error(f"Failed to connect to remote MySQL server. Details: {e}")
    internal_logger.critical("Website would not initialize.")
    exit()

internal_logger.info("Creating Flask app...")

app = Flask(__name__)
app.strict_slashes = False

internal_logger.info("Creating limiter...")

warnings.filterwarnings("ignore", message="Using the in-memory storage for tracking rate limits as no storage was explicitly specified.")

def get_ip_address():
    if request.headers.getlist('CF-Connecting-IP'):
        return request.headers.getlist("CF-Connecting-IP")[0]
    else:
        return request.remote_addr

limiter = Limiter(
    key_func=get_ip_address,
    app=app,
    default_limits=[]
)

internal_logger.info("Initializing classes...")

bcrypt = Bcrypt(app)

internal_logger.info("Initialized bcrypt (1 / 12).")

Signer = Signer(settings["PK1024Path"], settings["PK2048Path"])
internal_logger.info("Initialized script signer (2 / 12).")
Filter = TextFilter()
internal_logger.info("Initialized text filter (3 / 12).")
Tickets = Tickets(settings["PK1024Path"], settings["PK2048Path"])
internal_logger.info("Initialized tickets generator (4 / 12).")
UserDB = UserDB(Database, bcrypt)
internal_logger.info("Initialized users database (5 / 12).")
GamesDB = GamesDB(Database, settings["URL"])
internal_logger.info("Initialized games database (6 / 12).")
ArbiterClass = Arbiter(settings["arbiterURLs"], Database, GamesDB)
internal_logger.info("Initialized arbiter (class) (7 / 12).")
Assets = Assets(Database)
internal_logger.info("Initialized assets (class) (8 / 12).")
Token = Token()
internal_logger.info("Initialized safety token system (9 / 12).")
DataStore = DataStore(Database)
internal_logger.info("Initialized datastore (class) (10 / 12).")
Webhooks = Webhooks()
internal_logger.info("Initialized webhooks (class) (11 / 12).")
PointsService = PointsService(Database)
internal_logger.info("Initialized points service (class) (12 / 12).")

def includeRoutes():
    import mainRoutes.join
    import mainRoutes.fflags
    import mainRoutes.rootpath
    import mainRoutes.moderation
    import mainRoutes.v11
    import mainRoutes.v1
    import mainRoutes.login
    import mainRoutes.arbiter
    import mainRoutes.marketplace
    import mainRoutes.v2
    import mainRoutes.thumbs
    import mainRoutes.game
    import mainRoutes.universes
    import mainRoutes.underasset
    import mainRoutes.users
    import mainRoutes.sets
    import mainRoutes.persistence
    import mainRoutes.client
    import mainRoutes.uac
    import mainRoutes.abusereport
    import mainRoutes.ide
    import mainRoutes.points
    import mainRoutes.api
    
    internal_logger.info("Included 23 routes.")

internal_logger.info("Running logic...")

if __name__ == "__main__":
    internal_logger.info("Including routes...")
    includeRoutes()
    internal_logger.info("Running the application with hosting framework...")
    try:
        serve(TransLogger(app, setup_console_handler=False, logger=waitress_logger), listen='*:80', threads=24, channel_timeout=60, connection_limit=10000, expose_tracebacks=True)
    except Exception as e:
        internal_logger.critical(f"CRITICAL ERROR! Hosting framework has crashed. Details: {e}")
    internal_logger.info("Service shutting down...")
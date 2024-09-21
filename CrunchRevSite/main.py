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
import itertools
import gzip
import random
# import ssl
# import threading

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
print("---------------------------------------------------------------------------------")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

internal_logger = logging.getLogger('CrunchRev Internal Logs')
internal_logger.setLevel(logging.INFO)

internal_logger.info("Setting up logging...")

waitress_logger = logging.getLogger('waitress')
waitress_logger.setLevel(logging.INFO)

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

internal_logger.info("Initializing classes...")

bcrypt = Bcrypt(app)

Signer = Signer(settings["PK1024Path"], settings["PK2048Path"])
Filter = TextFilter()
Tickets = Tickets(settings["PK1024Path"], settings["PK2048Path"])
UserDB = UserDB(Database, bcrypt)
GamesDB = GamesDB(Database, settings["URL"])
ArbiterClass = Arbiter(settings["arbiterURLs"], Database, GamesDB)
Assets = Assets(Database)
Token = Token()
DataStore = DataStore(Database)

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

internal_logger.info("Running logic...")

if __name__ == "__main__":
    internal_logger.info("Including routes...")
    includeRoutes()
    internal_logger.info("Running the application with hosting framework...")
    try:
        serve(TransLogger(app, setup_console_handler=False, logger=waitress_logger), listen='*:80', ident=None, threads=24, channel_timeout=60, connection_limit=10000, expose_tracebacks=True)
    except Exception as e:
        internal_logger.critical(f"CRITICAL ERROR! Hosting framework has crashed. Details: {e}")
    internal_logger.info("Service shutting down...")

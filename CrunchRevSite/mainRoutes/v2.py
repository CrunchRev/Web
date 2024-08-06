"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under "/v2/" path
"""

from __main__ import *

@app.route("/v2/CreateOrUpdate/", methods=settings["HTTPMethods"])
def createorupdate():
    return {"success": True}, 200, {"Content-Type": "application/json"}
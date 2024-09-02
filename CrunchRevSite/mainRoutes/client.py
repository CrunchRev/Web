"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /client/
"""

from __main__ import *

@app.route("/client/pbe", methods=settings["HTTPMethods"])
def pbe():
    return "", 200

@app.route("/Counters/2ewds9i3uwed983223fd9wi3jedu3/<jobId>/update/<players>", methods=["GET"])
def updatecounters(jobId, players):
    ArbiterClass.updatePlayersOnJob(jobId, players)

    return {"success": True}, 200, {"Content-Type": "application/json"}
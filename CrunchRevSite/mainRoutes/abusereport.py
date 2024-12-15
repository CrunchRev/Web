"""
2024, Written by the CrunchRev Authors

Route module description: controls everything related to reports (sysstats and abuse reports)
"""

from __main__ import *

@app.route("/AbuseReport/InGameChatHandler.ashx", methods=["POST"])
def abuseReporter():
    reportXML = request.data.decode("utf-8") # I think it wouldn't be empty as it's not a JSON object, it's an XML

    # TODO: do db shit for that, now we just use webhook

    Webhooks.sendReportAbuse(reportXML)

    return "true", 200, {'Content-Type': 'text/plain'}

@app.route("/AbuseReport/sysstats/", methods=["GET"])
def sysstats():
    args = request.args
    gameId = args.get("gameId", 1)
    apiKey = args.get("apiKey", None)
    UserID = args.get("UserID", 1)
    Message = args.get("Message", "No message provided")
    Resolution = args.get("Resolution", "No resolution provided")

    if apiKey is None or apiKey != "4893weidsiu38324ewueir28":
        return "false", 200, {'Content-Type': 'text/plain'}

    Webhooks.sendSysStats(gameId, UserID, Message, Resolution)

    return "true", 200, {'Content-Type': 'text/plain'}
"""
2024, Written by the CrunchRev Authors

Route module description: controls everything related to reports (sysstats and abuse reports)
"""

from __main__ import *

@app.route("/AbuseReport/InGameChatHandler.ashx", methods=["POST"])
def abuseReporter():
    reportXML = request.data # I think it wouldn't be empty as it's not a JSON object, it's an XML

    # TODO: do db shit for that, now we just use webhook

    sendReportAbuse(reportXML)
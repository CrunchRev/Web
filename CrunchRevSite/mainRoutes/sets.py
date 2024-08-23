"""
2024, Written by the CrunchRev Authors

Route module description: controls everything related to sets
"""

from __main__ import *

@app.route("/game/Tools/InsertAsset.ashx", methods=settings["HTTPMethods"])
@app.route("/Game/Tools/InsertAsset.ashx", methods=settings["HTTPMethods"])
def insertAsset():
    query = request.query_string.decode("utf-8")

    builtURL = f"https://sets.pizzaboxer.xyz/Game/Tools/InsertAsset.ashx?{query}"
    requestSets = requests.get(builtURL)

    if requestSets.status_code == 200:
        return requestSets.text, 200, {"Content-Type": "application/xml"}
    else:
        return "Error: " + str(requestSets.status_code), requestSets.status_code, {"Content-Type": "text/plain"}
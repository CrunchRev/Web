"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /client/ and not only that
"""

from __main__ import *

@app.route("/client/pbe", methods=settings["HTTPMethods"])
def pbe():
    return "", 200

@app.route("/Counters/2ewds9i3uwed983223fd9wi3jedu3/<string:jobId>/update/<int:players>", methods=settings["HTTPMethods"])
def updatecounters(jobId, players):
    ArbiterClass.updatePlayersOnJob(jobId, players)
    return {"success": True}, 200, {"Content-Type": "application/json"}

@app.route("/ownership/hasasset", methods=settings["HTTPMethods"])
@app.route("/ownership/hasasset/", methods=settings["HTTPMethods"])
@app.route("/ownership/hasAsset", methods=settings["HTTPMethods"])
@app.route("/ownership/hasAsset/", methods=settings["HTTPMethods"])
def hasasset():
    trueOrFalse = "false"
    userId = int(request.args.get("userId"))
    assetId = int(request.args.get("assetId"))

    asyncFetch = Assets.owns(userId, assetId)

    if asyncFetch == True:
        trueOrFalse = "true"

    return trueOrFalse, 200, {'Content-Type': 'text/plain'}

@app.route("/currency/balance", methods=settings["HTTPMethods"])
def balance():
    cookiez = request.cookies
    info = None
    json = {}
    if (".ROBLOSECURITY" or "_ROBLOSECURITY") in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY") or cookiez.get("_ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)

    if not info:
        json = {"success": False}
    else:
        json = {
            "success": True,
            "robux": info[9],
            "tickets": info[9]
        }

    return jsonify(json), 200

@app.route("/device/initialize", methods=["POST"])
def init_the_device():
    return jsonify({"browserTrackerId":random.randint(1000, 1000000),"appDeviceIdentifier":None}), 200

@app.route("/mobileapi/check-app-version", methods=["GET"])
def check_app_ver():
    return jsonify({"data": {"UpgradeAction": "None"}}), 200
"""
2024 - 2025, Written by the CrunchRev Authors

Route module description: arbits the gameserver stuff on the web
"""

from __main__ import *
 
@app.route("/games/shutdown/", methods=settings["HTTPMethods"])
def shutdownGameserver():
    gameId = request.args.get("gameIdShutdown")

    if not gameId:
        return jsonify({"success": False, "error": "400, Please define game id."}), 400

    cookies = request.cookies
    user_info = None
    is_allowed = False
    game_data = GamesDB.fetchOne(gameId)

    if game_data["assets"] is None or game_data["info"] is None:
        return jsonify({"error": "404, The game does not exist."}), 404

    if ".ROBLOSECURITY" in cookies:
        cookie = cookies.get(".ROBLOSECURITY")
        user_info = UserDB.fetchUser(method=1, cookie=cookie)

        if not user_info:
            return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    else:
        return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400

    is_allowed = (user_info[0] == game_data["assets"][4]) or (user_info[8] == 1)

    if not is_allowed:
        return jsonify({"success": False, "error": "403, Access denied."}), 403

    return ArbiterClass.shutdownPlaceIdServers(gameId)

@app.route("/Arbiter/stopInstance.ashx", methods=settings["HTTPMethods"])
def stopInstance():
    jobId = request.args.get("jobId")
    access = request.args.get("access")

    if not jobId or not access:
        return jsonify({"success": False, "error": "400, Please define jobId and access as an access key."}), 400

    if access == "ddec2ab4ae78dda0bb3497b134ae5c61":
        return ArbiterClass.shutdownJobId(jobId)
    else:
        return jsonify({"success": False, "error": "403, Access denied."}), 403

@app.route("/v2.0/Refresh", methods=settings["HTTPMethods"])
def refresh():
    jobId = request.args.get("gameId")
    access = request.args.get("apiKey")
    players = request.args.get("clientCount")
    gameTime = request.args.get("gameTime")

    if not jobId or not access or not players or not gameTime:
        return jsonify({"success": False, "error": "400, Please define gameId as a job ID, apiKey as an access key, clientCount as players count and gameTime as time in float (ex. 15.0)."}), 400

    playersInt = int(players)
    timeFloat = float(gameTime)

    if playersInt < 1 and timeFloat >= 45.5: # making that so rcc doesnt shutdown just after it launched
        if access == "ddec2ab4ae78dda0bb3497b134ae5c61":
            return ArbiterClass.shutdownJobId(jobId)
        else:
            return jsonify({"success": False, "error": "403, Access denied."}), 403
    else:
        return jsonify({"success": True}), 200
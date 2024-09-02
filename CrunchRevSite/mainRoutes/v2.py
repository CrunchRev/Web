"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under "/v2/" path
"""

from __main__ import *

@app.route("/v2/CreateOrUpdate/", methods=settings["HTTPMethods"])
def createorupdate():
    jobId = request.args.get("gameId")
    access = request.args.get("apiKey")
    players = request.args.get("clientCount", type=int)

    if access == "ddec2ab4ae78dda0bb3497b134ae5c61":
        ArbiterClass.updatePlayersOnJob(jobId, players)

        return {"success": True}, 200, {"Content-Type": "application/json"}
    else:
        return jsonify({"success": False, "error": "403, Access denied."}), 403

@app.route("/v2/users/<playerId>/groups/roles", methods=settings["HTTPMethods"]) # we need that for admin icon ig
def rolez(playerId):
    user_info = UserDB.fetchUser(method=2, userId=playerId)

    if not user_info:
        return jsonify({"success": False, "message": "400, No user info found."}), 400

    is_an_admin = True if user_info[8] == 1 else False

    dataList = []

    if is_an_admin == True:
        for groupId in ["1200769", "3013794", "4358041"]:
            dataList.append(
                {
                    "group": {
                        "id": int(groupId),
                        "name": "string",
                        "memberCount": 0,
                        "hasVerifiedBadge": True,
                    },
                    "role": {
                        "id": int(groupId),
                        "rank": 255,
                        "name": "string",
                    },
                    "isNotificationsEnabled": True,
                }
            )

    json = {"data": dataList}

    return jsonify(json), 200
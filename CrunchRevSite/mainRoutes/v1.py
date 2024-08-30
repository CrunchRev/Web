"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /v1/
"""

from __main__ import *

@app.route("/v1/games/getAllGames/", methods=settings["HTTPMethods"])
def getAll():
    games = GamesDB.fetchAll()
    return jsonify(games)

# VisualPlugin sent me this endpoint for 2018 developer console
@app.route("/v1/user/<playerId>/is-admin-developer-console-enabled", methods=settings["HTTPMethods"])
@app.route("/v1/user/<playerId>/is-admin-developer-console-enabled/", methods=settings["HTTPMethods"])
def isDevConsoleEnabled2018L(playerId):
    user_info = UserDB.fetchUser(method=2, userId=playerId)

    is_an_admin = True if user_info[8] == 1 else False

    return jsonify({"isAdminDeveloperConsoleEnabled": user_info}), 200

@app.route("/v1/avatar-fetch", methods=settings["HTTPMethods"])
@app.route("/v1/avatar-fetch/", methods=settings["HTTPMethods"])
def avatar_fetch_v1():
    userId = request.args.get("userId", 0)
    userInfo = UserDB.fetchUser(method=2, userId=userId)

    json = {}
    charappItemzzz = []

    assetsCharAppFetch = Assets.fetchCharacterApperanceList(userId)

    if assetsCharAppFetch:
        for assetIdTuple in assetsCharAppFetch:
            assetId = assetIdTuple[0]
            charappItemzzz.append(assetId)

    if not userInfo:
        json = {"success": False, "message": "Unknown user or error while fetching."}
    else:
        avatarType = userInfo[10]
        json = {
            "resolvedAvatarType": str(avatarType),
            "equippedGearVersionIds": [],
            "backpackGearVersionIds": [],
            "accessoryVersionIds": charappItemzzz,
            "animations": {
                "Run": 969731563
            },
            "bodyColors": {
                "HeadColor": 194,
                "LeftArmColor": 194,
                "LeftLegColor": 102,
                "RightArmColor": 194,
                "RightLegColor": 102,
                "TorsoColor": 23
            },
            "scales": {
                "Height": 1,
                "Width": 1,
                "Head": 1,
                "Depth": 1,
                "Proportion": 0,
                "BodyType": 0
            }
        }

    return json, 200, {'Content-Type': 'application/json'}
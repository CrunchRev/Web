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
    """
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

    """

    json = {"resolvedAvatarType":"R15","equippedGearVersionIds":[],"backpackGearVersionIds":[],"assetAndAssetTypeIds":[{"assetId":301811432,"assetTypeId":12},{"assetId":607702162,"assetTypeId":8},{"assetId":607785314,"assetTypeId":11},{"assetId":10638267973,"assetTypeId":79},{"assetId":10647852134,"assetTypeId":78},{"assetId":12995014400,"assetTypeId":29},{"assetId":12995015868,"assetTypeId":30},{"assetId":12995017412,"assetTypeId":28},{"assetId":12995018829,"assetTypeId":31},{"assetId":12995020128,"assetTypeId":27}],"animationAssetIds":{"climb":2510230574,"fall":2510233257,"idle":2510235063,"jump":2510236649,"run":2510238627,"swim":2510240941,"walk":2510242378,"mood":10647852134},"bodyColors":{"headColorId":194,"torsoColorId":23,"rightArmColorId":194,"leftArmColorId":194,"rightLegColorId":102,"leftLegColorId":102},"scales":{"height":1.0,"width":1.0,"head":1.0,"depth":1.00,"proportion":0.0,"bodyType":0.0},"emotes":[]}

    return json, 200, {'Content-Type': 'application/json'}
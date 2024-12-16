"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /v1.1/
"""

from __main__ import *

@app.route("/v1.1/avatar-fetch", methods=settings["HTTPMethods"])
@app.route("/v1.1/avatar-fetch/", methods=settings["HTTPMethods"])
def avatar_fetch():
    userId = request.args.get("userId", 0, type=int)
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
        clrs = UserDB.fetchBodyColors(userId)

        labc = clrs[0]
        rabc = clrs[1]
        llbc = clrs[2]
        rlbc = clrs[3]
        tbc = clrs[4]
        hbc = clrs[5]

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
                "HeadColor": hbc,
                "LeftArmColor": labc,
                "LeftLegColor": llbc,
                "RightArmColor": rabc,
                "RightLegColor": rlbc,
                "TorsoColor": tbc
            },
            "bodyColorsUrl": f"http://assetgame.{settings["URL"]}/Asset/BodyColors.ashx?userId={userId}",
            "scales": {
                "Height": 1,
                "Width": 1,
                "Head": 1,
                "Depth": 1,
                "Proportion": 0,
                "BodyType": 0
            }
        }

    return jsonify(json), 200

@app.route("/v1.1/game-start-info", methods=settings["HTTPMethods"])
@app.route("/v1.1/game-start-info/", methods=settings["HTTPMethods"])
def startinfo():
    json = {"gameAvatarType":"PlayerChoice","allowCustomAnimations":"True","universeAvatarCollisionType":"OuterBox","universeAvatarBodyType":"Standard","jointPositioningType":"ArtistIntent","message":"","universeAvatarMinScales":{"height":0.9,"width":0.7,"head":0.95,"depth":0.0,"proportion":0.0,"bodyType":0.0},"universeAvatarMaxScales":{"height":1.05,"width":1.0,"head":1.0,"depth":0.0,"proportion":1.0,"bodyType":1.0},"universeAvatarAssetOverrides":[],"moderationStatus":None}

    return json, 200, {'Content-Type': 'application/json'}
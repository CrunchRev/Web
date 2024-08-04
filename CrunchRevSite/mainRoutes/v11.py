"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /v1.1/
"""

from __main__ import *

@app.route("/v1.1/avatar-fetch", methods=settings["HTTPMethods"])
@app.route("/v1.1/avatar-fetch/", methods=settings["HTTPMethods"])
def avatar_fetch():
    userId = request.args.get("userId") or "1"
    json = {
        "resolvedAvatarType": "R15",
        "equippedGearVersionIds": [],
        "backpackGearVersionIds": [],
        "accessoryVersionIds": [
            24112667
        ],
        "animations": {
            "Run": 969731563
        },
        "bodyColorsUrl": f"http://www.{settings["URL"]}/asset/BodyColors.ashx?userId={userId}",
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

@app.route("/v1.1/game-start-info", methods=settings["HTTPMethods"])
@app.route("/v1.1/game-start-info/", methods=settings["HTTPMethods"])
def startinfo():
    json = {"gameAvatarType":"PlayerChoice","allowCustomAnimations":"True","universeAvatarCollisionType":"OuterBox","universeAvatarBodyType":"Standard","jointPositioningType":"ArtistIntent","message":"","universeAvatarMinScales":{"height":0.9,"width":0.7,"head":0.95,"depth":0.0,"proportion":0.0,"bodyType":0.0},"universeAvatarMaxScales":{"height":1.05,"width":1.0,"head":1.0,"depth":0.0,"proportion":1.0,"bodyType":1.0},"universeAvatarAssetOverrides":[],"moderationStatus":None}

    return json, 200, {'Content-Type': 'application/json'}
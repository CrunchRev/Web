"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /v1/
"""

from __main__ import *

@app.route("/v1/games/getAllGames/", methods=settings["HTTPMethods"])
def getAll():
    games = GamesDB.fetchAll()
    return jsonify(games)

# VisualPlugin sent me this endpoint for developer console
@app.route("/v1/user/<playerId>/is-admin-developer-console-enabled", methods=settings["HTTPMethods"])
@app.route("/v1/user/<playerId>/is-admin-developer-console-enabled/", methods=settings["HTTPMethods"])
def isDevConsoleEnabled(playerId):
    user_info = UserDB.fetchUser(method=2, userId=playerId)

    is_an_admin = True if user_info[8] == 1 else False

    return jsonify({"isAdminDeveloperConsoleEnabled": is_an_admin}), 200

@app.route("/v1/avatar-fetch", methods=settings["HTTPMethods"])
@app.route("/v1/avatar-fetch/", methods=settings["HTTPMethods"])
def avatar_fetch_v1():
    userId = request.args.get("userId", 0, type=int)
    userInfo = UserDB.fetchUser(method=2, userId=userId)

    json = {}
    charappItemzzz = []

    assetsCharAppFetch = Assets.fetchCharacterApperanceList(userId)

    if assetsCharAppFetch:
        for assetIdTuple in assetsCharAppFetch:
            assetId = assetIdTuple[0]
            assetFetch = Assets.fetchAssetforAsset(assetId)
            assetType = assetFetch[1]
            charappItemzzz.append({"assetId": assetId, "assetTypeId": assetType})

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
            "assetAndAssetTypeIds": charappItemzzz,
            "animationAssetIds": {},
            "bodyColors": {
                "headColorId": hbc,
                "torsoColorId": tbc,
                "rightArmColorId": rabc,
                "leftArmColorId": labc,
                "rightLegColorId": rlbc,
                "leftLegColorId": llbc
            },
            "scales": {
                "height": 1.0,
                "width": 1.0,
                "head": 1.0,
                "depth": 1.0,
                "proportion": 0.0,
                "bodyType": 0.0
            },
            "emotes": []
        }

    return json, 200, {'Content-Type': 'application/json'}

@app.route("/v1/player-policies-client", methods=settings["HTTPMethods"])
def policies():
    json = {
        'isSubjectToChinaPolicies': False,
        'arePaidRandomItemsRestricted': False,
        'isPaidItemTradingAllowed': True,
        'areAdsAllowed': True,
    }

    return jsonify(json), 200

@app.route("/v1/users/<playerId>/friends", methods=settings["HTTPMethods"])
@app.route("/v1/users/<playerId>/friends/", methods=settings["HTTPMethods"])
def friends(playerId):
    return jsonify({"data": []}), 200

@app.route("/v1/presence/users", methods=settings["HTTPMethods"])
@app.route("/v1/presence/users/", methods=settings["HTTPMethods"])
def pplpersence():
    postData = request.json

    requestToAPI = requests.post("https://presence.roblox.com/v1/presence/users", json=postData)

    return jsonify(requestToAPI.json()), 200 # idk man what it returns so yeah (edit: https://presence.roblox.com/docs/index.html)

@app.route("/v1/batch", methods=settings["HTTPMethods"])
@app.route("/v1/batch/", methods=settings["HTTPMethods"])
def batch():
    # decoding taken from Syntax source,
    # please do not hate me.

    if request.headers.get("Content-Encoding") == "gzip":
        try:
            data = gzip.decompress(request.data)
        except Exception as e:
            return jsonify({"success": False, "message": "Invalid gzip data"}), 400
        try:
            JSONData = json.loads(data)
        except Exception as e:
            return jsonify({"success": False, "message": "Invalid JSON data"}), 400
    else:
        JSONData = request.json
    if JSONData is None:
        return jsonify({"success": False, "message": "Missing JSON data"}), 400
    
    # [{'requestId': 'type=GameIcon&id=1&w=128&h=128&filters=', 'targetId': 1, 'type': 'GameIcon', 'size': '128x128', 'isCircular': False}]
    # above is an example of return

    listOfReturn = []

    for object in JSONData:
        if "requestId" not in object or "targetId" not in object or "type" not in object or "size" not in object:
            continue
        if object["type"] not in [ "Avatar", "AvatarHeadShot", "GameIcon", "GameThumbnail", "Asset", "GroupIcon"]:
            continue
        
        targetId = object["targetId"]
        typeObj = object["type"]
        size = object["size"]
        requestId = object["requestId"] # used in json later

        url = None

        if typeObj == "GameThumbnail":
            fetchGamezzzz = GamesDB.fetchOne(targetId)

            if fetchGamezzzz["info"]:
                url = f"https://thumbscdn.{settings['URL']}/{fetchGamezzzz["info"][3]}"
            else:
                url = F"https://thumbscdn.{settings['URL']}/Default.png"
        elif typeObj == "GameIcon" or typeObj == "Asset":
            fetchGamezzzz = GamesDB.fetchOne(targetId)

            if fetchGamezzzz["info"]:
                url = f"https://thumbscdn.{settings['URL']}/{fetchGamezzzz["info"][4]}"
            else:
                url = F"https://thumbscdn.{settings['URL']}/DefaultIcon.png"
        elif typeObj == "Avatar":
            renderFile = ArbiterClass.render(targetId, 0, size.split("x")[0], size.split("x")[1], False)

            url = f"https://thumbscdn.{settings['URL']}/renders/{renderFile}"
        elif typeObj == "AvatarHeadShot":
            renderFile = ArbiterClass.render(targetId, 1, size.split("x")[0], size.split("x")[1], False)

            url = f"https://thumbscdn.{settings['URL']}/renders/{renderFile}"
        else:
            requestObject = requests.post("https://thumbnails.roblox.com/v1/batch", json=JSONData)

            return jsonify(requestObject.json()), 200

        listOfReturn.append({
            "requestId": requestId,
            "targetId": targetId,
            "state": "Completed",
            "imageUrl": url,
            "version": None
        })

    return jsonify({"data": listOfReturn}), 200

@app.route("/sign-out/v1", methods=["POST"])
def sign_out_v1():
    resp = make_response({"success": True})
    domain = f".{settings['URL']}"
    expiration = int(0)

    resp.set_cookie(key=".ROBLOSECURITY", value="", expires=expiration, domain=domain)

    resp.headers['Content-Type'] = 'application/json'

    return resp

@app.route("/v1/assets/batch", methods=settings["HTTPMethods"])
def assetsbatch():
    json = request.json

    returnRes = []

    for item in json:
        assetId = item["assetId"]
        assetType = str(item["assetType"])

        asset4asset = Assets.fetchAssetforAsset(assetId)

        if asset4asset:
            returnRes.append({
                "Location": f"https://www.{settings['URL']}/asset/?id={assetId}",
                "RequestId": str(uuid.uuid4())
            })
        else:
            continue

    return jsonify(returnRes), 200

        
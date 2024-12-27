"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /api/ (mostly CrunchRev Website APIs)
"""

from __main__ import *

# UTILITY FUNCTIONS

def rerender(userId):
    allRendersRes = ArbiterClass.getRerenderShit(userId)

    for res in allRendersRes:
        result1 = ArbiterClass.render(userId, res[2], res[0], res[1], True)

        if result1 is None:
            return False

    return True

@app.route("/api/editor/fetch", methods=["GET"])
def editor_fetch():
    cookies = request.cookies
    user_info = None

    if ".ROBLOSECURITY" in cookies:
        cookie = cookies.get(".ROBLOSECURITY")
        user_info = UserDB.fetchUser(method=1, cookie=cookie)

        if not user_info:
            return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    else:
        return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    
    userId = user_info[0]
    items = Assets.fetchAllAvatarItems(userId)

    return jsonify({"success": True, "items": items}), 200

@app.route("/api/editor/item/info", methods=["POST"])
def editor_item_info():
    jsonPayload = request.json
    itemAssetId = jsonPayload.get("itemId", None)

    if not itemAssetId:
        return jsonify({"success": False, "error": "400, Invalid request"}), 400
    
    name = Assets.fetchAssetName(itemAssetId)

    return jsonify({"success": True, "name": name, "image": f"https://www.{settings["URL"]}/Thumbs/Asset.ashx?AssetID={itemAssetId}", "id": itemAssetId}), 200

@app.route("/api/editor/bodycolors/fetch", methods=["GET"])
def editor_bodycolors_fetch():
    cookies = request.cookies
    user_info = None

    if ".ROBLOSECURITY" in cookies:
        cookie = cookies.get(".ROBLOSECURITY")
        user_info = UserDB.fetchUser(method=1, cookie=cookie)

        if not user_info:
            return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    else:
        return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    
    userId = user_info[0]

    clrs = UserDB.fetchBodyColors(userId)

    labc = clrs[0]
    rabc = clrs[1]
    llbc = clrs[2]
    rlbc = clrs[3]
    tbc = clrs[4]
    hbc = clrs[5]

    return jsonify({"success": True, "colors": [{"type": "Head", "brickcolor": hbc}, {"type": "Torso", "brickcolor": tbc}, {"type": "Left-Arm", "brickcolor": labc}, {"type": "Right-Arm", "brickcolor": rabc}, {"type": "Left-Leg", "brickcolor": llbc}, {"type": "Right-Leg", "brickcolor": rlbc}]}), 200

@app.route("/api/editor/items", methods=["POST"])
def editor_items():
    jsonPayload = request.json
    items = jsonPayload.get("items", None)
    action = jsonPayload.get("action", None)

    cookies = request.cookies
    user_info = None

    if ".ROBLOSECURITY" in cookies:
        cookie = cookies.get(".ROBLOSECURITY")
        user_info = UserDB.fetchUser(method=1, cookie=cookie)

        if not user_info:
            return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    else:
        return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    
    userId = user_info[0]

    owns = Assets.owns(userId, items[0])

    if not owns:
        return jsonify({"success": False, "error": "403, You don't own the item"}), 403

    # if not items or not action:
    #     return jsonify({"success": False, "error": "400, Invalid request"}), 400
    
    Assets.actionTheItem(userId=userId, assetId=items[0], action=action)
    
    return jsonify({"success": True, "items": items, "action": action}), 200

@app.route("/api/editor/bodycolors/colors", methods=["POST"])
def editor_bodycolors_colors():
    jsonPayload = request.json

    cookies = request.cookies
    user_info = None

    if ".ROBLOSECURITY" in cookies:
        cookie = cookies.get(".ROBLOSECURITY")
        user_info = UserDB.fetchUser(method=1, cookie=cookie)

        if not user_info:
            return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    else:
        return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    
    userId = user_info[0]

    labc = jsonPayload.get("left_arm", 1)
    rabc = jsonPayload.get("right_arm", 1)
    llbc = jsonPayload.get("left_leg", 1)
    rlbc = jsonPayload.get("right_leg", 1)
    tbc = jsonPayload.get("torso", 1)
    hbc = jsonPayload.get("head", 1)

    UserDB.updateBodyColors(userId, labc, rabc, llbc, rlbc, tbc, hbc)
    
    return jsonify({"success": True}), 200

@app.route("/api/editor/type/fetch", methods=["GET"])
def editor_type_fetch():
    cookies = request.cookies
    user_info = None

    if ".ROBLOSECURITY" in cookies:
        cookie = cookies.get(".ROBLOSECURITY")
        user_info = UserDB.fetchUser(method=1, cookie=cookie)

        if not user_info:
            return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    else:
        return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    
    avatarType = user_info[10]

    return jsonify({"success": True, "avatarType": avatarType}), 200

@app.route("/api/editor/type/change", methods=["POST"])
def editor_type_change():
    jsonPayload = request.json

    cookies = request.cookies
    user_info = None

    if ".ROBLOSECURITY" in cookies:
        cookie = cookies.get(".ROBLOSECURITY")
        user_info = UserDB.fetchUser(method=1, cookie=cookie)

        if not user_info:
            return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    else:
        return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    
    userId = user_info[0]

    avatarType = jsonPayload.get("avatarType", "R6")

    UserDB.updateAvatarType(userId, avatarType)
    
    return jsonify({"success": True}), 200

@app.route("/api/editor/avatar/rerender", methods=["GET"])
@limiter.limit("50 per minute")
def editor_avatar_rerender():
    cookies = request.cookies
    user_info = None

    if ".ROBLOSECURITY" in cookies:
        cookie = cookies.get(".ROBLOSECURITY")
        user_info = UserDB.fetchUser(method=1, cookie=cookie)

        if not user_info:
            return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    else:
        return jsonify({"success": False, "error": "400, You must sign in to use this feature"}), 400
    
    userId = user_info[0]
        
    result = ArbiterClass.render(userId, 0, 300, 300, True)

    thread = threading.Thread(target=rerender, args=(userId,))
    thread.start()

    return jsonify({"success": True, "image": f"https://thumbscdn.{settings['URL']}/renders/{result}"}), 200
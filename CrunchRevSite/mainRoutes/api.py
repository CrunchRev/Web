"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /api/ (mostly CrunchRev Website APIs)
"""

from __main__ import *

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

    return jsonify({"success": True, "name": name, "image": f"https://www.{settings["URL"]}/Thumbs/Asset.ashx?assetId={itemAssetId}", "id": itemAssetId}), 200

@app.route("/api/editor/bodycolors/fetch", methods=["GET"])
def editor_bodycolors_fetch():
    return jsonify({"success": True, "colors": [{"type": "Head", "brickcolor": 194}, {"type": "Torso", "brickcolor": 23}, {"type": "Left-Arm", "brickcolor": 194}, {"type": "Right-Arm", "brickcolor": 194}, {"type": "Left-Leg", "brickcolor": 102}, {"type": "Right-Leg", "brickcolor": 102}]}), 200

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

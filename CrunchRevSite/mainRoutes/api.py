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

@app.route("/api/editor/item/fetch", methods=["POST"])
def editor_item_fetch():
    jsonPayload = request.json
    itemAssetId = jsonPayload.get("itemId", None)

    if not itemAssetId:
        return jsonify({"success": False, "error": "400, Invalid request"}), 400
    
    name = Assets.fetchAssetName(itemAssetId)

    return jsonify({"success": True, "name": name, "image": "https://via.placeholder.com/100", "id": itemAssetId}), 200
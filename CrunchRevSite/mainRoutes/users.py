"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /users/
"""

from __main__ import *

@app.route("/users/<playerId>/canmanage/<placeId>", methods=settings["HTTPMethods"])
@app.route("/users/<playerId>/canmanage/<placeId>/", methods=settings["HTTPMethods"])
def ownership(playerId, placeId):
    user_info = UserDB.fetchUser(method=2, userId=playerId)
    game_data = GamesDB.fetchOne(placeId)

    if game_data["assets"] is None or game_data["info"] is None or user_info is None:
        return jsonify({"error": "404, The game or user does not exist."}), 404

    ownership = (user_info[0] == game_data["assets"][4]) or (user_info[8] == 1)

    return jsonify({"Success": True, "CanManage": ownership}), 200

@app.route("/users/<playerId>/friends", methods=settings["HTTPMethods"])
def friendsList(playerId):
    return jsonify({"data": []}), 200

@app.route("/userblock/getblockedusers", methods=["GET"])
def getBlockedUsers():
    return jsonify({
        "success": True,
        "userList": [],
        "total": 0
    }), 200

@app.route("/user/multi-following-exists", methods=['POST'])
def multiFollowingExists():
    return jsonify({
        "followings": [],
    }), 200

@app.route("/user/following-exists", methods=["GET"])
def followingExists():
    return jsonify({"success": True, "isFollowing": False}), 200
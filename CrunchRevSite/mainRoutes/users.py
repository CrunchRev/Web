"""
2024 - 2025, Written by the CrunchRev Authors

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

@app.route("/users/account-info", methods=["GET"])
def accountInfoEnd():
    cookiez = request.cookies
    info = None
    if (".ROBLOSECURITY" or "_ROBLOSECURITY") in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY") or cookiez.get("_ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
    else:
        return jsonify({"success": False}), 200
    
    if info is None:
        return jsonify({"success": False}), 200
    
    userName = info[1]
    userId = info[0]
    crunchesBalance = info[9]

    return jsonify({
        "UserId": userId,
        "Username": userName,
        "DisplayName": userName,
        "HasPasswordSet": True,
        "Email": None,
        "AgeBracket": 0,
        "Roles": [],
        "MembershipType": "None",
        "RobuxBalance": crunchesBalance,
        "NotificationCount": 0,
        "EmailNotificationEnabled": False,
        "PasswordNotificationEnabled": False
    }), 200
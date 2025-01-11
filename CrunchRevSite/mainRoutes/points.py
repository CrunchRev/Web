"""
2024 - 2025, Written by the CrunchRev Authors

Route module description: controls everything under "/points/" path
"""

from __main__ import *

@app.route("/points/get-point-balance", methods=["GET"])
def get_point_balance():
    userId = request.args.get(key="userId", default=0, type=int)
    placeId = request.args.get(key="placeId", default=0, type=int)

    user = UserDB.fetchUser(method=2, userId=userId)

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    place = GamesDB.fetchOne(placeId)

    if not place["assets"] or not place["info"]:
        return jsonify({"success": False, "message": "Place not found"}), 404
    
    fetchedPoints = int(PointsService.getPoints(userId, placeId))

    return jsonify({"success": True, "pointBalance": fetchedPoints}), 200

@app.route("/points/get-points-leaderboard", methods=["GET"])
def get_points_leaderboard():
    placeId = request.args.get(key="placeId", default=0, type=int)

    data = []

    place = GamesDB.fetchOne(placeId)

    if not place["assets"] or not place["info"]:
        return jsonify({"success": False, "message": "Place not found"}), 404
    
    fetchedLeaderboard = PointsService.getPointsLeaderboard(placeId)

    if fetchedLeaderboard:
        for stats in fetchedLeaderboard:
            userId = stats[0]
            points = stats[2]
            
            user = UserDB.fetchUser(method=2, userId=userId)

            if not user:
                continue

            username = user[1]

            data.append({
                "userId": userId,
                "username": username,
                "avatarImage": f"https://www.{settings["URL"]}/staticContent/Placeholder.png",
                "points": points
            })

    return jsonify({"success": True, "leaderboard": data}), 200

@app.route("/points/award-points", methods=["POST"])
def award_points():
    userId = request.args.get(key="userId", default=0, type=int)
    placeId = request.args.get(key="placeId", default=0, type=int)
    amount = request.args.get(key="amount", default=0, type=int)

    ip_address = request.headers.getlist("CF-Connecting-IP")[0]

    if not ip_address in settings["whitelistedPlaceIPs"]:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    user = UserDB.fetchUser(method=2, userId=userId)

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    place = GamesDB.fetchOne(placeId)

    if not place["assets"] or not place["info"]:
        return jsonify({"success": False, "message": "Place not found"}), 404
    
    PointsService.awardPoints(userId, placeId, amount)

    fetchedPoints = int(PointsService.getPoints(userId, placeId))

    return jsonify({"success": True, "userBalance": fetchedPoints, "pointsAwarded": amount, "userGameBalance": fetchedPoints}), 200
"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /marketplace/
"""

from __main__ import *

@app.route("/marketplace/productinfo", methods=settings["HTTPMethods"])
@app.route("/marketplace/productinfo/", methods=settings["HTTPMethods"])
@app.route("/marketplace/productInfo", methods=settings["HTTPMethods"])
@app.route("/marketplace/productInfo/", methods=settings["HTTPMethods"])
@app.route("/marketplace/productDetails", methods=settings["HTTPMethods"])
@app.route("/marketplace/productDetails/", methods=settings["HTTPMethods"]) # adding these two because they are the same (?)
def prodInfo():
    assetId = int(request.args.get("assetId") or request.args.get("productId"))

    if not assetId:
        return jsonify({"success": False, "message": "400, Please specify assetId argument."}), 400

    gameData = GamesDB.fetchOne(assetId)
    assetsData = None

    try:
        assetsData = gameData["assets"]
    except:
        pass

    if not assetsData or not gameData:
        # we just request shit from roblox API then
        # https://apis.roblox.com/game-passes/v1/game-passes/GAMEPASS-ID/product-info

        requestURL = f"https://apis.roblox.com/game-passes/v1/game-passes/{assetId}/product-info"
        requestResource = None
        requestJSON = {}
        try:
            requestResource = requests.get(requestURL)
            requestJSON = requestResource.json()
        except:
            return jsonify({"error": "Error while getting JSON response from Roblox API."})
        
        return jsonify(requestJSON), 200

    name = assetsData[1]
    description = assetsData[2]
    creatorId = int(assetsData[4])

    creatorName = UserDB.fetchUser(method=2, userId=creatorId)[1]

    createdAt = assetsData[5]
    updatedAt = assetsData[6]
    is_for_sale = assetsData[9]

    if is_for_sale == 1:
        is_for_sale = True
    else:
        is_for_sale = False

    return jsonify({
        "AssetId": assetId,
        "ProductId": assetId,
        "Name": str(name),
        "Description": str(description),
        "AssetTypeId": 9,
        "Creator": {
            "Id": creatorId,
            "Name": str(creatorName),
            "CreatorType": "User",
            "CreatorTargetId": creatorId
        },
        "IconImageAssetId": assetId,
        "Created": str(createdAt),
        "Updated": str(updatedAt),
        "PriceInRobux": None,
        "PriceInTickets": None,
        "Sales": 0,
        "IsNew": False,
        "IsForSale": is_for_sale,
        "IsPublicDomain": False,
        "IsLimited": False,
        "IsLimitedUnique": False,
        "Remaining": None,
        "MinimumMembershipLevel": 0,
        "ContentRatingTypeId": 0
    }), 200
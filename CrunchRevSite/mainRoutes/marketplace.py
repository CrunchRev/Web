"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /marketplace/
"""

from __main__ import *

@app.route("/marketplace/productinfo", methods=settings["HTTPMethods"])
def prodInfo():
    assetId = int(request.args.get("assetId"))

    if not assetId:
        return {"success": False, "message": "400, Please specify assetId argument."}, 400, {"Content-Type": "application/json"}

    gameData = GamesDB.fetchOne(assetId)

    if not gameData:
        return {"success": False, "message": "404, Game does not exist."}, 404, {"Content-Type": "application/json"}

    assetsData = gameData["assets"]

    if not assetsData:
        return {"success": False, "message": "404, Game does not exist."}, 404, {"Content-Type": "application/json"}

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

    return {
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
    }, 200, {"Content-Type": "application/json"}
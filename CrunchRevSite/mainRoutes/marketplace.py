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
        # https://economy.roblox.com/v2/assets/{assetId}/details

        requestURL = f"https://economy.roblox.com/v2/assets/{assetId}/details"

        requestResource = None
        requestJSON = {}
        try:
            # fuck roblox for ratelimiting guest requests, using an empty account

            cookiesForRequest = {".ROBLOSECURITY": settings["ROBLOSECURITY_cookie"]}

            requestResource = requests.get(requestURL, cookies=cookiesForRequest)
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

@app.route("/marketplace/purchase", methods=["POST"]) # expects POST from the logs
def purchaseShit():
    form_data = request.form
    gamepass_id = int(form_data.get('productId'))

    cookiez = request.cookies
    cookie = None
    info = None
    if (".ROBLOSECURITY" or "_ROBLOSECURITY") in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY") or cookiez.get("_ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)

    currentBalance = int(info[9])
    price = 50 # TODO: retrieve price from the database

    if price > currentBalance:
        return jsonify({"status": "error", "error": "Too poor!"})

    UserDB.removeSomeCurrency(price, cookie)

    time.sleep(0.5)
    
    return jsonify({"success": True, "status": "Bought"})
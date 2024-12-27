"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under thumbnails path
"""

from __main__ import *

@app.route("/Thumbs/GameIcon.ashx", methods=settings["HTTPMethods"])
def GameIcon():
    assetId = request.args.get("assetId")
    fetchGamezzzz = GamesDB.fetchOne(assetId)

    if fetchGamezzzz["info"]:
        return redirect(f"https://thumbscdn.{settings['URL']}/{fetchGamezzzz["info"][3]}")
    else:
        return redirect(F"https://thumbscdn.{settings['URL']}/Default.png")

@app.route("/asset-thumbnail/json", methods=settings["HTTPMethods"])
@app.route("/asset-thumbnail/json/", methods=settings["HTTPMethods"])
def jsonasset():
    json = {"Url":f"http://www.{settings["URL"]}/Thumbs/GameIcon.ashx","Final":True,"SubstitutionType":0}
    return json, 200, {'Content-Type': 'application/json'}

@app.route("/avatar-thumbnail/json", methods=settings["HTTPMethods"])
@app.route("/avatar-thumbnail/json/", methods=settings["HTTPMethods"])
def jsonthumb():
    user_id = request.args.get('userId', default='1')
    width = request.args.get('width', default='420')

    renderFile = ArbiterClass.render(user_id, 0, width, width, False)

    url = f"https://thumbscdn.{settings['URL']}/renders/{renderFile}"

    return jsonify({"data":[{"targetId":1,"state":"Completed","imageUrl":url,"version":"TN3"}]})

@app.route("/Thumbs/Avatar.ashx", methods=settings["HTTPMethods"])
@app.route("/thumbs/avatar.ashx", methods=settings["HTTPMethods"])
def imagethumb():
    user_id = request.args.get('userId', default='1')
    width = request.args.get('width', default='420')

    renderFile = ArbiterClass.render(user_id, 0, width, width, False)

    url = f"https://thumbscdn.{settings['URL']}/renders/{renderFile}"

    return redirect(url)

@app.route("/Thumbs/Headshot.ashx", methods=settings["HTTPMethods"])
@app.route("/thumbs/headshot.ashx", methods=settings["HTTPMethods"])
def imagethumbheadshot():
    user_id = request.args.get('userId', default='1')
    width = request.args.get('width', default='420')

    renderFile = ArbiterClass.render(user_id, 1, width, width, False)

    url = f"https://thumbscdn.{settings['URL']}/renders/{renderFile}"

    return redirect(url)

@app.route("/Thumbs/Asset.ashx", methods=settings["HTTPMethods"])
@app.route("/thumbs/asset.ashx", methods=settings["HTTPMethods"])
def image2thumb():
    asset_id = request.args.get('AssetID', default='1818')
    width = request.args.get('Width', default='420')
    height = request.args.get('Height', default='420')
    url = f"https://thumbnails.roblox.com/v1/assets?assetIds={asset_id}&returnPolicy=PlaceHolder&format=PNG&size={width}x{height}&isCircular=false"
    response = requests.get(url)

    if not response.status_code == 200:
        return jsonify({"success": False}), response.status_code

    image_url = response.json()['data'][0]['imageUrl']
    return redirect(image_url)

@app.route("/avatar-thumbnail/image", methods=settings["HTTPMethods"])
@app.route("/avatar-thumbnail/image/", methods=settings["HTTPMethods"])
def image3thumb():
    user_id = request.args.get('userId', default='1')
    width = request.args.get('width', default='420')

    renderFile = ArbiterClass.render(user_id, 0, width, width, False)

    url = f"https://thumbscdn.{settings['URL']}/renders/{renderFile}"

    return redirect(url)

@app.route("/bust-thumbnail/json", methods=settings["HTTPMethods"])
@app.route("/bust-thumbnail/json/", methods=settings["HTTPMethods"])
def json2thumb():
    user_id = request.args.get('userId', default='1')
    width = request.args.get('width', default='420')

    renderFile = ArbiterClass.render(user_id, 1, width, width, False)

    url = f"https://thumbscdn.{settings['URL']}/renders/{renderFile}"

    return redirect(url)
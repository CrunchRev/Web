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
        return redirect(f"/staticContent/thumbnailGamesStorage/{fetchGamezzzz["info"][3]}")
    else:
        return redirect("/staticContent/thumbnailGamesStorage/Default.png")

@app.route("/asset-thumbnail/json", methods=settings["HTTPMethods"])
def jsonasset():
    json = {"Url":f"http://www.{settings["URL"]}/Thumbs/GameIcon.ashx","Final":True,"SubstitutionType":0}
    return json, 200, {'Content-Type': 'application/json'}
"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under "/universes/" path
"""

from __main__ import *

@app.route("/universes/get-universe-containing-place", methods=settings["HTTPMethods"])
@app.route("/universes/get-universe-containing-place/", methods=settings["HTTPMethods"])
def g_u_c_p():
    placeId = request.args.get("placeid", "1")
    return jsonify({"UniverseId": placeId}), 200

@app.route("/universes/rc", methods=settings["HTTPMethods"])
@app.route("/universes/rc/", methods=settings["HTTPMethods"])
@app.route("/universes/validate-place", methods=settings["HTTPMethods"])
@app.route("/universes/validate-place-join", methods=settings["HTTPMethods"])
@app.route("/universes/validate-place/", methods=settings["HTTPMethods"])
@app.route("/universes/validate-place-join/", methods=settings["HTTPMethods"])
def universial_func():
    return "true", 200, {'Content-Type': "text/plain"}

@app.route("/universes/get-info", methods=settings["HTTPMethods"])
@app.route("/universes/get-info/", methods=settings["HTTPMethods"])
def get_info():
    return jsonify({"Name":"Classic: Crossroads","Description":"The classic ROBLOX level is back!","RootPlace":1818,"StudioAccessToApisAllowed":True,"CurrentUserHasEditPermissions":False,"UniverseAvatarType":"PlayerChoice"}), 200

@app.route("/universes/<placeId:placeId>/cloudeditenabled", methods=settings["HTTPMethods"])
def cloudedit(placeId):
    return jsonify({"enabled": False}), 200
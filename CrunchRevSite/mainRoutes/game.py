"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under "/game/" path (joinscript stuff not included)
"""

from __main__ import *

@app.route('/game/LuaWebService/HandleSocialRequest.ashx', methods=settings["HTTPMethods"])
@app.route('/Game/LuaWebService/HandleSocialRequest.ashx', methods=settings["HTTPMethods"])
def processsocialrequest():
    method = request.args.get('method', 'IsFriendsWith')
    groupid = request.args.get('groupid', '1200769')
    playerid = request.args.get('playerid', '1337')

    user_info = UserDB.fetchUser(method=2, userId=playerid)

    if not user_info:
        return jsonify({"success": False, "message": "400, No user info found."}), 400

    is_an_admin = True if user_info[8] == 1 else False

    root = ET.Element('Value')
    if method == "IsBestFriendsWith":
        root.set('Type', 'boolean')
        root.text = 'false'
    elif method == "IsFriendsWith":
        root.set('Type', 'boolean')
        root.text = 'false'
    elif method == "IsInGroup":
        root.set('Type', 'boolean')
        if groupid in ["1200769", "3013794", "4358041"]:
            root.text = 'true' if is_an_admin else 'false'
        else:
            root.text = 'false'
    elif method == "GetGroupRank":
        root.set('Type', 'integer')
        if groupid in ["1200769", "3013794", "4358041"]:
            root.text = '255' if is_an_admin else '0'
        else:
            root.text = '0'
    else:
        root.set('Type', 'string')
        root.text = 'No method found.'

    xml_response = ET.tostring(root, encoding='utf-8', method='xml')
    return Response(xml_response, mimetype='text/xml')

@app.route("/game/GetCurrentUser.ashx", methods=settings["HTTPMethods"])
def getcurruser():
    cookiez = request.cookies
    cookie = None
    info = None
    if (".ROBLOSECURITY" or "_ROBLOSECURITY") in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY") or cookiez.get("_ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)

    userid = info[0] if info else 13

    logging.info(str(userid))

    response = Response(str(userid), status=200, mimetype="text/plain")

    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    response.headers['Last-Modified'] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    return response

@app.route("/game/logout.aspx", methods=settings["HTTPMethods"])
def log_theoutwithaspx():
    resp = make_response(f'<meta http-equiv="refresh" content="0; url=https://www.{settings["URL"]}/login">') # redirect doesnt work, so yeah
    domain = f".{settings['URL']}"
    expiration = int(0)

    resp.set_cookie(key=".ROBLOSECURITY", value="", expires=expiration, domain=domain)

    return resp
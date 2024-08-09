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
        if groupid == "1200769":
            root.text = 'true' if is_an_admin else 'false'
        else:
            root.text = 'false'
    elif method == "GetGroupRank":
        root.set('Type', 'integer')
        if groupid == "1200769":
            root.text = '255' if is_an_admin else '0'
        else:
            root.text = '0'
    else:
        root.set('Type', 'string')
        root.text = 'No method found.'

    xml_response = ET.tostring(root, encoding='utf-8', method='xml')
    return Response(xml_response, mimetype='text/xml')
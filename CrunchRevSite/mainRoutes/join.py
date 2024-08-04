"""
2024, Written by the CrunchRev Authors

Route module description: controls placelauncher, joinscript stuff
"""

from __main__ import *

@app.route("/game/join.ashx", methods=settings["HTTPMethods"])
def joinashx():
    cookiez = request.cookies
    username = "Player1"
    userid = 0
    placeIDarg = request.args.get("placeId")
    jobIDarg = request.args.get("jobId")

    ticket = None
    signed = None
    if ".ROBLOSECURITY" in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        
        if info:
            username = info[1]
            userid = info[0]
    
    if not (placeIDarg or jobIDarg):
        return {"error": "400, No jobId or placeId was set."}, 400

    fetchJobID = ArbiterClass.getInformationViaJobID(jobIDarg)
    fetchGameInfo = GamesDB.fetchOne(placeIDarg)

    if not fetchJobID or not (fetchGameInfo["assets"] or fetchGameInfo["info"]):
        return {"error": "400, No information about that jobId or game was found."}, 400

    is_roblox_place = (fetchGameInfo["assets"][4] == 1)
    
    if fetchGameInfo["info"][1] == "2018L":
        ticket = Tickets.generate_client_ticket_v2(userid, username, f'http://www.{settings["URL"]}/asset/CharacterFetch.ashx?userId={userid}', jobIDarg)
    else:
        ticket = Tickets.generate_client_ticket_v1(userid, username, jobIDarg)

    joinScript = json.dumps({
        "ClientPort": 0,
        "MachineAddress": fetchJobID[5],
        "ServerPort": fetchJobID[4],
        "PingUrl": "",
        "PingInterval": 120,
        "UserName": f"{username}",
        "SeleniumTestMode": False,
        "UserId": userid,
        "SuperSafeChat": False,
        "CharacterAppearance": f"http://www.{settings["URL"]}/asset/CharacterFetch.ashx?userId=1",
        "ClientTicket": f"{ticket}",
        "GameId": jobIDarg,
        "PlaceId": int(placeIDarg),
        "MeasurementUrl": "",
        "WaitingForCharacterGuid": f"{uuid.uuid4()}",
        "BaseUrl": f"http://www.{settings["URL"]}/",
        "ChatStyle": "ClassicAndBubble",
        "VendorId": 0,
        "ScreenShotInfo": "",
        "VideoInfo": "",
        "CreatorId": fetchGameInfo["assets"][4],
        "CreatorTypeEnum": "User",
        "MembershipType": "None",
        "AccountAge": 1000,
        "CookieStoreFirstTimePlayKey": "rbx_evt_ftp",
        "CookieStoreFiveMinutePlayKey": "rbx_evt_fmp",
        "CookieStoreEnabled": True,
        "IsRobloxPlace": is_roblox_place,
        "GenerateTeleportJoin": False,
        "IsUnknownOrUnder13": False,
        "SessionId": f"SessionId-{uuid.uuid4()}",
        "GameChatType": "AllUsers",
        "DataCenterId": 0,
        "UniverseId": placeIDarg,
        "BrowserTrackerId": 0,
        "UsePortraitMode": False,
        "FollowUserId": 0,
        "CountryCode": "US"
    })

    if fetchGameInfo["info"][1] == "2018L":
        signed = Signer.sign_v2("\r\n" + joinScript)
    else:
        signed = Signer.sign_v1("\r\n" + joinScript)

    return signed, 200, {'Content-Type': 'text/plain'}

@app.route("/game/PlaceLauncher.ashx", methods=settings["HTTPMethods"])
def launchtheplace():
    cookiez = request.cookies
    cookiers = None
    is_allowed = False
    is_for_sale = False
    info = None
    if ".ROBLOSECURITY" in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        if info:
            cookiers = cookie

    placeIDarg = request.args.get("placeId")

    if not placeIDarg:
        return {"error": "400, No placeId is set."}, 400

    game_data = GamesDB.fetchOne(placeIDarg)

    if not info == None:
        is_allowed = (info[0] == game_data["assets"][4]) or (info[8] == 1)
    
    is_for_sale = (game_data["assets"][8] == 1)

    if not is_for_sale:
        if not is_allowed:
            return jsonify({"error": "403, You are not allowed to view this game."}), 403

    year = game_data["info"][1]

    logging.info(f"PlaceLauncher requested, args: {placeIDarg}")
    logging.info("Getting server details...")

    # print(year)
    # print(placeIDarg)

    PlaceLauncherRequest = ArbiterClass.requestServer(year, placeIDarg)

    status = 0
    jobID = None
    joinScriptURL = ""
    message = None

    logging.info("Successfully got information, returning to user")

    if 'success' in PlaceLauncherRequest:
        status = PlaceLauncherRequest['status']
        message = PlaceLauncherRequest['message']
        if not status in [0, 1, 4, 3]:
            jobID = PlaceLauncherRequest['jobId']
            joinScriptURL = f"http://www.{settings["URL"]}/game/join.ashx?placeId={placeIDarg}&jobId={jobID}"

    json = {
        "jobId": jobID,
        "status": status,
        "joinScriptUrl": joinScriptURL,
        "authenticationUrl": f"http://www.{settings["URL"]}/Login/Negotiate.ashx",
        "authenticationTicket": f"{cookiers}",
        "message": message
    }

    return json, 200, {'Content-Type': 'application/json'}

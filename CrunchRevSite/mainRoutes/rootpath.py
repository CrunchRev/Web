"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under "/" path
"""

from __main__ import *

@app.before_request
def bef_req():
    logging.info(f"Request host: {request.host}")
    if f"setup.{settings["URL"]}" in request.host:
        file_path = request.path.lstrip('/')
        local_path = os.path.join(app.root_path, "staticContentSetup")
        return send_from_directory(local_path, file_path, as_attachment=True)
    elif f"thumbscdn.{settings["URL"]}" in request.host:
        file_path = request.path.lstrip('/')
        local_path = os.path.join(app.root_path, "staticContentThumbs")
        return send_from_directory(local_path, file_path, as_attachment=True)
    
    cookiez = request.cookies
    if ".ROBLOSECURITY" in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        
        if info:
            is_banned = info[5] == 1

            if is_banned:
                if not request.path.lstrip('/') in ["not-approved", "tos", "logout"] and not "staticContent" in request.path.lstrip('/') and not "validate-machine" in request.path.lstrip('/'):
                    return redirect("/not-approved")
    
@app.errorhandler(404)
def notfound(e):
    if not "setup.unirev.xyz" in request.host or not "thumbscdn.unirev.xyz" in request.host:
        loggedIn = False
        info = None
        cookiez = request.cookies
        if ".ROBLOSECURITY" in cookiez:
            cookie = cookiez.get(".ROBLOSECURITY")
            info = UserDB.fetchUser(method=1, cookie=cookie)
            
            if info:
                loggedIn = True

        return render_template("notfound.html", userinfo=info, baseurl=settings["URL"], loggedIn=loggedIn), 404
    else:
        return "<p>404, Not found.</p>", 404

@app.route("/", methods=settings["HTTPMethods"])
def root():
    cookiez = request.cookies
    if ".ROBLOSECURITY" in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        
        if info:
            return redirect("/home")
        else:
            return redirect("/login")
    else:
        return redirect("/login")

@app.route("/staticContent/<path:path>", methods=settings["HTTPMethods"])
def serveStatic(path):
    return send_from_directory('staticContent', path)

@app.route("/home", methods=settings["HTTPMethods"])
def home():
    cookiez = request.cookies
    info = None
    loggedIn = False
    if ".ROBLOSECURITY" in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        
        if info:
            loggedIn = True
        else:
            return redirect("/login")
    else:
        return redirect("/login")

    return render_template("home.html", userinfo=info, baseurl=settings["URL"], loggedIn=loggedIn)

@app.route("/games", methods=settings["HTTPMethods"])
def games():
    cookiez = request.cookies
    info = None
    loggedIn = False
    if ".ROBLOSECURITY" in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        
        if info:
            loggedIn = True

    return render_template("games.html", userinfo=info, baseurl=settings["URL"], loggedIn=loggedIn)

@app.route("/games/<gameid>", methods=settings["HTTPMethods"])
def game(gameid):
    cookies = request.cookies
    user_info = None
    is_logged_in = False
    is_roblox_app = False
    is_allowed = False
    game_data = GamesDB.fetchOne(gameid)

    if game_data["assets"] is None or game_data["info"] is None:
        return jsonify({"error": "404, The game does not exist."}), 404

    user_agent = request.headers.get('User-Agent')
    if user_agent:
        is_roblox_app = "ROBLOX Android App" in user_agent or "ROBLOX iOS App" in user_agent
    else:
        is_roblox_app = False

    if ".ROBLOSECURITY" in cookies:
        cookie = cookies.get(".ROBLOSECURITY")
        user_info = UserDB.fetchUser(method=1, cookie=cookie)

        if user_info:
            is_logged_in = True
        else:
            return redirect("/login")
    else:
        return redirect("/login")

    is_allowed = (user_info[0] == game_data["assets"][4]) or (user_info[8] == 1)
    is_for_sale = (game_data["assets"][8] == 1)
    counters = game_data["countersPlayers"]

    if not is_for_sale:
        if not is_allowed:
            return jsonify({"error": "403, You are not allowed to view this game."}), 403

    dev_info = UserDB.fetchUser(2, userId=game_data["assets"][4])

    return render_template(
        "game.html",
        userinfo=user_info,
        baseurl=settings["URL"],
        loggedIn=is_logged_in,
        placeid=game_data["info"][0],
        isRobloxApp=is_roblox_app,
        gamename=game_data["assets"][1],
        gameclient=game_data["info"][1],
        creatorid=game_data["assets"][4],
        creatorname=dev_info[1],
        isAllowed=is_allowed,
        description=game_data["assets"][2],
        currplayers=counters,
        maxPlayers=game_data["info"][2],
        createdAt=game_data["assets"][5],
        updatedAt=game_data["assets"][6],
        visits=game_data["info"][5]
    )

@app.route("/logout", methods=settings["HTTPMethods"])
def log_theout():
    resp = make_response(f'<meta http-equiv="refresh" content="0; url=https://www.{settings["URL"]}/login">') # redirect doesnt work, so yeah
    domain = f".{settings['URL']}"
    expiration = int(0)

    resp.set_cookie(key=".ROBLOSECURITY", value="", expires=expiration, domain=domain)

    return resp

@app.route("/login", methods=settings["HTTPMethods"])
def login():
    cookiez = request.cookies
    loggedIn = False
    if ".ROBLOSECURITY" in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        
        if info:
            loggedIn = True

    if (loggedIn):
        return redirect("/home")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        passedToken = request.form.get("safetyToken") or ""

        if Token.checkToken(passedToken) is False:
            return jsonify({"message": "Invalid safety token, try regoing to the page. 400"}), 400

        loggedInResult, cookie = UserDB.login(username, password)

        if loggedInResult is True:
            resp = make_response(f'<meta http-equiv="refresh" content="0; url=https://www.{settings["URL"]}/home">') # redirect doesnt work, so yeah
            domain = f".{settings['URL']}"
            expiration = int(time.time() + (365 * 24 * 60 * 60))

            resp.set_cookie(key=".ROBLOSECURITY", value=cookie, expires=expiration, domain=domain, samesite='Lax')

            return resp
        else:
            return jsonify({"message": "Invalid username or password, 400"}), 400

    safety_token = Token.generateToken()

    return render_template("login.html", baseurl=settings["URL"], safety_token=safety_token), 200

@app.route("/signup", methods=settings["HTTPMethods"])
def signup():
    cookiez = request.cookies
    loggedIn = False
    if ".ROBLOSECURITY" in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        
        if info:
            loggedIn = True

    if (loggedIn):
        return redirect("/home")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        invite_key = request.form.get("invkey")
        repeat_password = request.form.get("repeat-password")
        passedToken = request.form.get("safetyToken") or ""

        if Token.checkToken(passedToken) is False:
            return jsonify({"message": "Invalid safety token, try regoing to the page. 400"}), 400

        if password == repeat_password:
            signUpResult, cookie = UserDB.signup(username, password, invite_key)

            if signUpResult is True:
                resp = make_response(f'<meta http-equiv="refresh" content="0; url=https://www.{settings["URL"]}/home">') # redirect doesnt work, so yeah
                domain = f".{settings['URL']}"
                expiration = int(time.time() + (365 * 24 * 60 * 60))

                resp.set_cookie(key=".ROBLOSECURITY", value=cookie, expires=expiration, domain=domain, samesite='Lax')

                return resp
            else:
                return jsonify({"message": "Not valid username or invite key. Make sure the username is unique, does not contain spaces. It must be 20 characters maximum and 3 characters minimum. Not allowed usernames (check is case-insensitive): Roblox. Also make sure your invite key is valid. It might be also an internal error. 400"}), 400
        else:
            return jsonify({"message": "Passwords do not match. 400"}), 400

    safety_token = Token.generateToken()

    return render_template("signup.html", baseurl=settings["URL"], safety_token=safety_token), 200

@app.route("/Asset/", methods=settings["HTTPMethods"])
@app.route("/Asset", methods=settings["HTTPMethods"])
@app.route("/asset/", methods=settings["HTTPMethods"])
@app.route("/asset", methods=settings["HTTPMethods"])
@app.route("/v1/asset", methods=settings["HTTPMethods"])
@app.route("/v1/asset/", methods=settings["HTTPMethods"])
def assetdelivery():
    idarg = 1818

    try:
        idarg = int(request.args.get("id") or request.args.get("assetversionid") or 1818)
    except:
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    local_path = os.path.join(app.root_path, "LocalAssets")
    local_file_path = os.path.join(local_path, str(idarg))
        
    # ip_address = request.headers.getlist("X-Real-IP")[0]

    ip_address = request.remote_addr

    if os.path.isfile(local_file_path):
        return send_from_directory(local_path, str(idarg))

    asset_info = Assets.fetchAssetforAsset(int(idarg))

    if asset_info:
        is_allowed = False
        cookies = request.cookies
        user_info = None

        if ".ROBLOSECURITY" in cookies:
            cookie = cookies.get(".ROBLOSECURITY")
            user_info = UserDB.fetchUser(method=1, cookie=cookie)

        if asset_info[1] == 9:
            if user_info:
                is_allowed = (user_info[0] == asset_info[2]) or (user_info[8] == 1)

            if is_allowed or (ip_address in settings["whitelistedPlaceIPs"]):
                return send_from_directory("C:/assets_cdn_crunchrev/", asset_info[0])
            else:
                return jsonify({"success": False, "error": "403, Access denied."}), 403
        else:
            return send_from_directory("C:/assets_cdn_crunchrev/", asset_info[0])

    assetRemoteURL = f"https://assetdelivery.roblox.com/v1/asset?id={idarg}"
    
    try:
        cookieRequest = {".ROBLOSECURITY": settings["ROBLOSECURITY_cookie"]}
        response = requests.get(assetRemoteURL, cookies=cookieRequest)
        response.raise_for_status()
    except requests.RequestException:
        return redirect(assetRemoteURL)
    
    binaryData = response.content
    AssetResponse = Response(binaryData, content_type='application/octet-stream')

    AssetResponse.headers['Expires'] = '0'
    AssetResponse.headers['Cache-Control'] = 'must-revalidate'
    AssetResponse.headers['Pragma'] = 'public'
    AssetResponse.headers['Content-Description'] = 'File Transfer'
    AssetResponse.headers['Content-Disposition'] = f'attachment; filename={idarg}'
    AssetResponse.headers['Content-Length'] = str(len(binaryData))

    return AssetResponse

@app.route("/GetAllowedSecurityVersions/", methods=settings["HTTPMethods"])
def secfunc1():
    return '{"data":[""INTENRALandroidapp"","0.235.0pcplayer", "0.360.0pcplayer"]}', 200, {'Content-Type': 'text/plain'}

@app.route("/GetAllowedMD5Hashes/", methods=settings["HTTPMethods"])
def secfunc2():
    return {"data":["9473e6c1287eec31332884f6d1f1766e", "c5157659313d1213afe032fab30823db"]}, 200, {'Content-Type': 'application/json'}

@app.route("/GetAllowedSecurityKeys/", methods=settings["HTTPMethods"])
def secfunc3():
    return {"data":[]}, 200, {'Content-Type': 'application/json'}

@app.route("/robots.txt", methods=settings["HTTPMethods"])
def robots():
    return """User-agent: *

Disallow: /
Disallow: */wp-includes/*
Disallow: */wp-json/
Disallow: */wp-admin/
Disallow: */wp
Disallow: */wp-content/
Disallow: *.php""", 200, {'Content-Type': 'text/plain'}

@app.route("/favicon.ico", methods=settings["HTTPMethods"])
def favicon():
    return send_from_directory('staticContent', "CrunchRevAsset1.png"), 200, {'Content-Type': 'image/png'}

@app.route("/download", methods=settings["HTTPMethods"])
def downloadakaredirect():
    return redirect("https://discord.gg/6ruRdK9zkv")

@app.route("/Games.aspx", methods=settings["HTTPMethods"])
@app.route("/Games", methods=settings["HTTPMethods"])
@app.route("/games/", methods=settings["HTTPMethods"])
def redirecttogames():
    return redirect("/games")

@app.route("/settings", methods=settings["HTTPMethods"])
def settingsendpoint():
    return jsonify({"ok": 1}), 200 # I don't know what it returns

@app.route("/not-approved", methods=settings["HTTPMethods"])
def bannedScreen():
    cookiez = request.cookies
    info = None
    loggedIn = False
    if ".ROBLOSECURITY" in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        
        if not info:
            return redirect("/login")
        else:
            loggedIn = True
    else:
        return redirect("/login")
    
    is_banned = info[5] == 1

    if not is_banned:
        return redirect("/home")
    
    ban_reason = info[6]

    return render_template("not-approved.html", userinfo=info, baseurl=settings["URL"], loggedIn=loggedIn, banReason=ban_reason), 403

@app.route("/pe.png", methods=settings["HTTPMethods"])
@app.route("/pe", methods=settings["HTTPMethods"])
@app.route("/pe/", methods=settings["HTTPMethods"])
def pe_endpoint():
    query = request.query_string.decode("utf-8")
    
    new_url = f'https://ecsv2.roblox.com/pe?{query}'
    response = requests.get(new_url)
    
    if 200 <= response.status_code < 300:
        return response.text, response.status_code, {'Content-Type': 'text/plain'}
    else:
        return f'Request error: {response.status_code}', response.status_code, {'Content-Type': 'text/plain'}
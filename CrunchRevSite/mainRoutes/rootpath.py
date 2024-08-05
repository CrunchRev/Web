"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under "/" path
"""

from __main__ import *

@app.errorhandler(InternalServerError)
def handle_500_error(error):
    error_dict = {
        'code': error.code,
        'description': error.description,
        'stack_trace': traceback.format_exc()
    }
    return render_template('error_page.html', **error_dict)

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
        currplayers=0,
        maxPlayers=game_data["info"][2],
        createdAt=game_data["assets"][5]
    )

@app.route("/Logout/", methods=settings["HTTPMethods"])
def log_theout():
    resp = make_response("Success! <a href='/login'>Login</a>")
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
        loggedInResult, cookie = UserDB.login(username, password)

        if loggedInResult is True:
            resp = make_response("Success! <a href='/games'>Get started!</a>", 200)
            domain = f".{settings['URL']}"
            expiration = int(time.time() + (365 * 24 * 60 * 60))

            resp.set_cookie(key=".ROBLOSECURITY", value=cookie, expires=expiration, domain=domain)

            return resp
        else:
            return jsonify({"message": "Invalid username or password, 400"}), 400

    return render_template("login.html"), 200

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

    """

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        loggedInResult, cookie = UserDB.login(username, password)

        if loggedInResult is True:
            resp = make_response("Success! <a href='/games'>Get started!</a>", 200)
            domain = f".{settings['URL']}"
            expiration = int(time.time() + (365 * 24 * 60 * 60))

            resp.set_cookie(key=".ROBLOSECURITY", value=cookie, expires=expiration, domain=domain)

            return resp
        else:
            return jsonify({"message": "Invalid username or password, 400"}), 400
            
    """

    return render_template("signup.html"), 200

@app.route("/Asset/", methods=settings["HTTPMethods"])
@app.route("/Asset", methods=settings["HTTPMethods"])
@app.route("/asset/", methods=settings["HTTPMethods"])
@app.route("/asset", methods=settings["HTTPMethods"])
def assetdelivery():
    idarg = int(request.args.get("id") or request.args.get("assetversionid") or 1818)
    user_agent = request.headers.get("User-Agent") or "Default"
    accesskey = request.args.get("access") or "NoAccessKey"

    local_path = os.path.join(app.root_path, "LocalAssets")
    local_file_path = os.path.join(local_path, str(idarg))

    if os.path.isfile(local_file_path):
        return send_from_directory(local_path, str(idarg))

    asset_info = None
    try:
        asset_info = Assets.fetchAssetforAsset(int(idarg))
    except Exception as e:
        logging.error(f"Error fetching asset info from DB: {e}")
        asset_info = None

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

            if is_allowed or accesskey == "ddec2ab4ae78dda0bb3497b134ae5c61" or user_agent == "Roblox/WinInet":
                return send_from_directory("C:/assets_cdn_crunchrev/", asset_info[0])
            else:
                return jsonify({"success": False, "error": "403, Access denied."}), 403
        else:
            return send_from_directory("C:/assets_cdn_crunchrev/", asset_info[0])

    return redirect(f"https://assetdelivery.roblox.com/v1/asset?id={idarg}")

# we count that as root due to it is in asset

@app.route("/Asset/BodyColors.ashx", methods=settings["HTTPMethods"])
def bodycolors():
    return """<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">
  <External>null</External>
  <External>nil</External>
  <Item class="BodyColors">
    <Properties>
      <int name="HeadColor">194</int>
      <int name="LeftArmColor">194</int>
      <int name="LeftLegColor">102</int>
      <string name="Name">Body Colors</string>
      <int name="RightArmColor">194</int>
      <int name="RightLegColor">102</int>
      <int name="TorsoColor">23</int>
      <bool name="archivable">true</bool>
    </Properties>
  </Item>
</roblox>""", 200, {'Content-Type': 'text/xml'}

@app.route("/GetAllowedSecurityVersions/", methods=settings["HTTPMethods"])
def secfunc1():
    return {"data":["0.235.0pcplayer", "0.360.0pcplayer"]}, 200, {'Content-Type': 'application/json'}

@app.route("/GetAllowedMD5Hashes/", methods=settings["HTTPMethods"])
def secfunc2():
    return {"data":["477466d51a0290a0c37d4932bb91af67", "6537957e30bf1c1f67c8cfafd095218c"]}, 200, {'Content-Type': 'application/json'}

@app.route("/GetAllowedSecurityKeys/", methods=settings["HTTPMethods"])
def secfunc3():
    return "true", 200, {'Content-Type': 'text/plain'}

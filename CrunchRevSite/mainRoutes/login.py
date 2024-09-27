"""
2024, Written by the CrunchRev Authors

Route module description: controls Negotiate.ashx and other stuff related to login (not the page)
"""

from __main__ import *

@app.route("/Login/Negotiate.ashx", methods=settings["HTTPMethods"])
def NegotiateClient():
    suggestarg = request.args.get("suggest")
    if not suggestarg:
        return "false"
    else:
        # idk = idk # triggering 500 error
        validation = UserDB.fetchUser(method=1, cookie=suggestarg)
        # print(validation)
        if not validation:
            return "false"
        else:
            resp = make_response(suggestarg, 200)
            resp.headers["Content-Type"] = "text/plain"
            domain = f".{settings['URL']}"
            expiration = int(time.time() + (365 * 24 * 60 * 60))

            resp.set_cookie(key=".ROBLOSECURITY", value=suggestarg, expires=expiration, domain=domain, samesite='Lax')

            return resp

@app.route("/game/validate-machine", methods=settings["HTTPMethods"])
@app.route("/game/validate-machine/", methods=settings["HTTPMethods"])
def validate():
    cookiez = request.cookies
    is_banned = False
    if ".ROBLOSECURITY" in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        
        if info:
            is_banned = info[5] == 1

    return jsonify({"success": is_banned == False}), 200
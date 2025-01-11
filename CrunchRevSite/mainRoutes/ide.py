"""
2024 - 2025, Written by the CrunchRev Authors

Route module description: controls everything under /ide/
"""

from __main__ import *

@app.route("/ide/welcome", methods=["GET"])
def welcomeide():
    ownGamesBasedOnCookie = []
    cookiez = request.cookies

    if (".ROBLOSECURITY" or "_ROBLOSECURITY") in cookiez:
        cookie = cookiez.get(".ROBLOSECURITY") or cookiez.get("_ROBLOSECURITY")
        info = UserDB.fetchUser(method=1, cookie=cookie)
        
        if info:
            userId = int(info[0])
            ownGamesBasedOnCookie = GamesDB.fetchAllPlacesWhereCreatorIdIs(userId, '2016E')

    return render_template("welcomeide.html", ownGamesBasedOnCookie=ownGamesBasedOnCookie)

@app.route("/IDE/ClientToolbox.aspx", methods=["GET"])
def redirclienttoolbox():
    return redirect("/ide/clienttoolbox")

@app.route("/ide/clienttoolbox", methods=["GET"])
def clienttoolbox():
    return render_template("clienttoolbox.html"), 200
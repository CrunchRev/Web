"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /v1/
"""

from __main__ import *

@app.route("/v1/games/getAllGames/", methods=settings["HTTPMethods"])
def getAll():
    games = GamesDB.fetchAll()
    return jsonify(games)

# VisualPlugin sent me this endpoint for 2018 developer console
@app.route("/v1/user/<playerId>/is-admin-developer-console-enabled", methods=settings["HTTPMethods"])
@app.route("/v1/user/<playerId>/is-admin-developer-console-enabled/", methods=settings["HTTPMethods"])
def isDevConsoleEnabled2018L(playerId):
    return jsonify({"isAdminDeveloperConsoleEnabled": True}), 200
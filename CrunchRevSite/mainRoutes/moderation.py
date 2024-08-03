"""
2024, Written by the CrunchRev Authors

Route module description: controls everything needed for chat
"""

from __main__ import *

@app.route("/moderation/filtertext/", methods=settings["HTTPMethods"])
@app.route("/moderation/filtertext", methods=settings["HTTPMethods"])
def moderate():
    unfilteredText = request.form.get("text") or "This is fucking text. Бля чуваки, меня так всё заебало что аж пиздец."
    moderated = Filter.censor(unfilteredText)
    json = {
        "data": {
            "white": str(unfilteredText),
            "black": str(moderated)
        }
    }

    return json, 200, {'Content-Type': 'application/json'}

@app.route("/moderation/v2/filtertext/", methods=settings["HTTPMethods"])
@app.route("/moderation/v2/filtertext", methods=settings["HTTPMethods"])
@app.route("/moderation/v2/", methods=settings["HTTPMethods"])
@app.route("/moderation/v2", methods=settings["HTTPMethods"])
@app.route("/moderation/v2/filter/text/", methods=settings["HTTPMethods"])
@app.route("/moderation/v2/filter/text", methods=settings["HTTPMethods"])
def moderatev2():
    unfilteredText = request.form.get("text") or "This is fucking text. Бля чуваки, меня так всё заебало что аж пиздец."
    moderated = Filter.censor(unfilteredText)
    jsonv2 = {
        "success": True,
        "message": "",
        "data": {
            "AgeUnder13": moderated,
            "Age13OrOver": moderated
        }
    }

    return jsonv2, 200, {'Content-Type': 'application/json'}

@app.route("/game/players/<player>", methods=settings["HTTPMethods"])
@app.route("/game/players/<player>/", methods=settings["HTTPMethods"])
def modefilter(player):
    return {"ChatFilter":"blacklist"}, 200, {'Content-Type': 'application/json'}
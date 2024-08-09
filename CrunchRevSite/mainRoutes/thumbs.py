"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under "/Thumbs/" path
"""

from __main__ import *

@app.route("/Thumbs/GameIcon.ashx", methods=settings["HTTPMethods"])
def GameIcon():
    return redirect("/staticContent/thumbnailForPlaces.png")
"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /client/
"""

from __main__ import *

@app.route("/client/pbe", methods=settings["HTTPMethods"])
def pbe():
    return "", 200
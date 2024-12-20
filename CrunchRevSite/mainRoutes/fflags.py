"""
2024, Written by the CrunchRev Authors

Route module description: controls client settings (feature or fast flags)
"""

from __main__ import *

@app.route("/Setting/QuietGet/<settingstype>/", methods=settings["HTTPMethods"])
def setting(settingstype):
    path = f'{settings["FFlagsPath"]}{settingstype}.json'

    if not os.path.exists(path):
        return jsonify({}), 404
    
    with open(path, 'r') as file:
        file = file.read()
        file = file.replace("roblox.com", settings["URL"])
    
    return jsonify(file), 200

@app.route("/Setting/2018LGet/<settingstype>/", methods=settings["HTTPMethods"])
def setting2018Llegcacy(settingstype):
    path = f'{settings["FFlags2018LPath"]}{settingstype}.json'
    if not os.path.exists(path):
        return jsonify({}), 404
    
    with open(path, 'r') as file:
        file = file.read()
        file = file.replace("roblox.com", settings["URL"])
    
    return jsonify(file), 200

@app.route("/v1/settings/application", methods=settings["HTTPMethods"])
@app.route("/v1/settings/application/", methods=settings["HTTPMethods"])
def setting2021E():
    typeOfFFlag = request.args.get("applicationName") or "PCDesktopClient"
    path = f'{settings["FFlags2021EPath"]}{typeOfFFlag}.json'

    if not os.path.exists(path):
        return jsonify({}), 404
    
    with open(path, 'r') as file:
        file = file.read()
        file = file.replace("roblox.com", settings["URL"])
    
    return jsonify(file), 200
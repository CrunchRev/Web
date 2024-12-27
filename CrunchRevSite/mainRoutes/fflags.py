"""
2024, Written by the CrunchRev Authors

Route module description: controls client settings (feature or fast flags)
"""

from __main__ import *

@app.route("/Setting/QuietGet/<settingstype>/", methods=settings["HTTPMethods"])
def setting_legacy(settingstype):
    path = f'{settings["FFlagsPath"]}{settingstype}.json'

    if not os.path.exists(path):
        return jsonify({}), 404
    
    with open(path, 'r') as file:
        file = file.read()
        file = file.replace("roblox.com", settings["URL"])
        file = json.loads(file)
    
    return jsonify(file), 200

@app.route("/Setting/2018LGet/<settingstype>/", methods=settings["HTTPMethods"])
@app.route("/Setting/Get/<settingstype>/", methods=settings["HTTPMethods"])
def setting_standard(settingstype):
    path = f'{settings["FFlags2018LPath"]}{settingstype}.json'
    if not os.path.exists(path):
        return jsonify({}), 404
    
    with open(path, 'r') as file:
        file = file.read()
        file = file.replace("roblox.com", settings["URL"])
        file = json.loads(file)
    
    return jsonify(file), 200

@app.route("/v1/settings/application", methods=settings["HTTPMethods"])
@app.route("/v1/settings/application/", methods=settings["HTTPMethods"])
def setting_modern():
    typeOfFFlag = request.args.get("applicationName", "PCDesktopClient")
    path = f'{settings["FFlags2021EPath"]}{typeOfFFlag}.json'

    if not os.path.exists(path):
        return jsonify({}), 404
    
    with open(path, 'r') as file:
        file = file.read()
        file = file.replace("roblox.com", settings["URL"])
        file = json.loads(file)
    
    return jsonify(file), 200
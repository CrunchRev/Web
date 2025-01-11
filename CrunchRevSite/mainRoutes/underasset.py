"""
2024 - 2025, Written by the CrunchRev Authors

Route module description: controls everything under "/asset/" path
"""

from __main__ import *

@app.route("/Asset/BodyColors.ashx", methods=settings["HTTPMethods"])
def bodycolors():
    userId = request.args.get("userId", 0, type=int)

    fetchUser = UserDB.fetchUser(method=2, userId=userId)

    if not fetchUser:
        return jsonify({"success": False, "message": "400, No user info found."}), 400

    clrs = UserDB.fetchBodyColors(userId)

    labc = clrs[0]
    rabc = clrs[1]
    llbc = clrs[2]
    rlbc = clrs[3]
    tbc = clrs[4]
    hbc = clrs[5]

    return f"""<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">
  <External>null</External>
  <External>nil</External>
  <Item class="BodyColors">
    <Properties>
      <int name="HeadColor">{hbc}</int>
      <int name="LeftArmColor">{labc}</int>
      <int name="LeftLegColor">{llbc}</int>
      <string name="Name">Body Colors</string>
      <int name="RightArmColor">{rabc}</int>
      <int name="RightLegColor">{rlbc}</int>
      <int name="TorsoColor">{tbc}</int>
      <bool name="archivable">true</bool>
    </Properties>
  </Item>
</roblox>""", 200, {'Content-Type': 'text/xml'}

@app.route("/Asset/CharacterFetch.ashx", methods=settings["HTTPMethods"])
@app.route("/asset/CharacterFetch.ashx", methods=settings["HTTPMethods"])
def old_characterappearance():
    userId = request.args.get("userId", 0, type=int)
    charapp = f"http://www.{settings["URL"]}/Asset/BodyColors.ashx?userId={str(userId)};"

    assetsCharAppFetch = Assets.fetchCharacterApperanceList(userId)

    if assetsCharAppFetch:
        for assetIdTuple in assetsCharAppFetch:
            assetId = assetIdTuple[0]
            charapp = charapp + f"http://www.{settings["URL"]}/Asset/?id={assetId};"

    return charapp, 200, {'Content-Type': 'text/plain'}
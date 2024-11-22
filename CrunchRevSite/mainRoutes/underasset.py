"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under "/asset/" path
"""

from __main__ import *

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

@app.route("/Asset/CharacterFetch.ashx", methods=settings["HTTPMethods"])
@app.route("/asset/CharacterFetch.ashx", methods=settings["HTTPMethods"])
def old_characterappearance():
    userId = request.args.get("userId", 0)
    charapp = f"http://www.{settings["URL"]}/Asset/BodyColors.ashx?userId={str(userId)};"

    assetsCharAppFetch = Assets.fetchCharacterApperanceList(userId)

    if assetsCharAppFetch:
        for assetIdTuple in assetsCharAppFetch:
            assetId = assetIdTuple[1]
            charapp = charapp + f"http://www.{settings["URL"]}/Asset/?id={assetId};"

    return charapp, 200, {'Content-Type': 'text/plain'}
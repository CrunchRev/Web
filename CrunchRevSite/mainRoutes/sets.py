"""
2024 - 2025, Written by the CrunchRev Authors

Route module description: controls everything related to sets
"""

from __main__ import *

@app.route("/game/Tools/InsertAsset.ashx", methods=settings["HTTPMethods"])
@app.route("/Game/Tools/InsertAsset.ashx", methods=settings["HTTPMethods"])
def insertAsset():
    query = request.query_string.decode("utf-8")

    builtURL = f"https://sets.pizzaboxer.xyz/Game/Tools/InsertAsset.ashx?{query}"
    requestSets = requests.get(builtURL)

    if requestSets.status_code == 200:
        return requestSets.text, 200, {"Content-Type": "application/xml"}
    else:
        return "Error: " + str(requestSets.status_code), requestSets.status_code, {"Content-Type": "text/plain"}

@app.route("/game/Tools/ThumbnailAsset.ashx", methods=settings["HTTPMethods"])
@app.route("/Game/Tools/ThumbnailAsset.ashx", methods=settings["HTTPMethods"])
def thumbnailAsset():
    aid = request.args.get('aid', '')
    wd = request.args.get('wd', 75, type=int)
    ht = request.args.get('ht', 75, type=int)

    wd = wd if wd > 0 else 75
    ht = ht if ht > 0 else 75

    if aid and aid.isalnum():
        url = f"https://thumbnails.roblox.com/v1/assets?assetIds={aid}&returnPolicy=PlaceHolder&size={wd}x{ht}&format=Png&isCircular=false"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0 and 'imageUrl' in data['data'][0]:
                image_url = data['data'][0]['imageUrl']
                if requests.utils.urlparse(image_url).scheme in ['http', 'https']:
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        return send_file(BytesIO(image_response.content), mimetype='image/png')
                    else:
                        return jsonify({"error": "Unable to fetch image from the provided URL"}), 500
                else:
                    return jsonify({"error": "Invalid image URL"}), 400
            else:
                return jsonify({"error": "URL not found in returned data"}), 404
        else:
            return jsonify({"error": "Unable to fetch data from the Roblox API"}), 500
    else:
        return jsonify({"error": "Invalid or missing asset ID"}), 400
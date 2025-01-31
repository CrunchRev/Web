"""
2024 - 2025, Written by the CrunchRev Authors

Route module description: controls everything under "/persistence/" path
"""

from __main__ import *

logger = logging.getLogger(__name__)

@app.route("/persistence/set", methods=["POST"])
def setPersistence():
    query = request.args
    form_data = request.form

    placeId = query.get("placeId", type=int)

    checkPlace = GamesDB.fetchOne(placeId)

    if (checkPlace["info"] or checkPlace['assets']) is None:
        return jsonify({"data":[], "message": "Place does not exist"}), 200

    scope = query.get('scope', 'global')
    target = query.get('target')
    key = query.get('key')

    if (len(scope) or len(target) or len(key)) > 50:
        logging.warning("Scope, target or key exceeded 50 characters limit, aborting...")
        return jsonify({"data": None, "message": "Scope, target or key exceeds limit of 50 characters."}), 400

    value_str = form_data.get('value', 'null')
    value = json.loads(value_str)

    if len(value_str) > 4 * 1024 * 1024: # 4 megabytes as official roblox limit: There are limits to how much data you can send to datastores per minute […] - and that limit is 4MB.
        logging.warning("Value exceeded 4 MB limit, aborting...")
        return jsonify({"data": None, "message": "Value exceeds limit of four megabytes."}), 400

    logger.info(f"Setting data with scope: {scope}, target: {target}, key: {key}, value: {value}, placeId: {str(placeId)}")

    check = DataStore.doesExist(scope, target, key, placeId)

    if check == False:
        DataStore.insertData(scope, target, key, value, placeId)
    else:
        DataStore.editData(scope, target, key, value, placeId)

    return jsonify({"data": value}), 200

@app.route('/persistence/getv2', methods=["POST"])
@app.route('/persistence/getV2', methods=["POST"])
# @app.route('/persistence/getSortedValues', methods=["POST"]) # this one will have other format
def getVersion2():
    form_data = request.form

    placeId = request.args.get("placeId", type=int)

    checkPlace = GamesDB.fetchOne(placeId)

    if (checkPlace["info"] or checkPlace['assets']) is None:
        return jsonify({"data":[], "message": "Place does not exist"}), 200

    return_data = []
    starting_count = 0

    while True:
        prefix = f"qkeys[{starting_count}]"
        scope = form_data.get(f"{prefix}.scope", 'global')
        target = form_data.get(f"{prefix}.target")
        key = form_data.get(f"{prefix}.key")
        
        if target is None or key is None:
            break

        if (len(scope) or len(target) or len(key)) > 50:
            logging.warning("Scope, target or key exceeded 50 characters limit, aborting...")
            return jsonify({"data":[], "message": "Scope, target or key exceeds limit of 50 characters."}), 400

        logger.info(f"Retrieving data for scope: {scope}, target: {target}, key: {key}, placeId: {str(placeId)}")

        result = DataStore.getData(scope, target, key, placeId)

        if result is None:
            break

        logger.info(f"Retrieved data for scope: {scope}, target: {target}, key: {key}, placeId: {str(placeId)}, result: {result}")

        return_data.append({
            "Value": result,
            "Scope": str(scope),
            "Key": str(key),
            "Target": str(target),
        })

        logger.info("Appended.")

        starting_count += 1

    if len(return_data) == 0:
        logger.warning("Not found the datastore query in the database.")
        return jsonify({"data":[], "message": "No data being requested"}), 200
    
    data = {"data":return_data}
    logger.info(f"Data: {data}")
    
    return jsonify(data), 200
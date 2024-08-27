"""
2024, Written by the CrunchRev Authors

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

    value_str = form_data.get('value', 'null')
    value = json.loads(value_str)

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

        logger.info(f"Retrieving data for scope: {scope}, target: {target}, key: {key}, placeId: {str(placeId)}")

        result = DataStore.getData(scope, target, key, placeId)

        if result is None:
            # gonna experiment with that \/ \/ \/

            break

            """
                DataStore.setData(scope, target, key, "0")
                result = DataStore.getData(scope, target, key)
            """

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
        logger.warning("No data being requested.")
        return jsonify({"data":[], "message": "No data being requested"}), 200
    
    data = {"data":return_data}
    logger.info(f"Data: {data}")
    
    return jsonify(data), 200
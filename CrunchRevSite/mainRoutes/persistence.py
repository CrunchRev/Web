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

    scope = query.get('scope', 'global')
    target = query.get('target')
    key = query.get('key')

    value_str = form_data.get('value', 'null')
    value = json.loads(value_str)

    logger.info(f"Setting data with scope: {scope}, target: {target}, key: {key}, value: {value}")
    
    DataStore.setData(scope, target, key, value)
    return jsonify({"data": value}), 200

@app.route('/persistence/getv2', methods=["POST"])
@app.route('/persistence/getV2', methods=["POST"])
# @app.route('/persistence/getSortedValues', methods=["POST"]) # this one will have other format
def getVersion2():
    form_data = request.form

    return_data = []
    starting_count = 0

    while True:
        prefix = f"qkeys[{starting_count}]"
        scope = form_data.get(f"{prefix}.scope", 'global')
        target = form_data.get(f"{prefix}.target")
        key = form_data.get(f"{prefix}.key")
        
        if target is None or key is None:
            break

        result = DataStore.getData(scope, target, key)

        if result is None:
            # gonna experiment with that \/ \/ \/

            # break

            DataStore.setData(scope, target, key, "0")
            result = DataStore.getData(scope, target, key)

        logger.info(f"Retrieved data for scope: {scope}, target: {target}, key: {key}, result: {result}")

        return_data.append({
            "Value": str(result),
            "Scope": str(scope),
            "Key": str(key),
            "Target": str(target),
        })

        starting_count += 1

    if not return_data:
        logger.warning("No data being requested.")
        return jsonify({"data": [], "message": "No data being requested"}), 200
    
    data = {"data": return_data}
    logger.info(f"Data: {data}")
    
    return jsonify(data), 200
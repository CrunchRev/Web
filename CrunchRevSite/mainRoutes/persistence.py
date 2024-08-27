"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under "/persistence/" path
"""

from __main__ import *

@app.route("/persistence/set", methods=["POST"])
def setPersistence():
    query = request.args
    form_data = request.form

    scope = query.get('scope', 'global')
    target = query.get('target')
    key = query.get('key')

    value_str = form_data.get('value', 'null')
    value = json.loads(value_str)

    DataStore.setData(scope, target, key, value)
    return jsonify({"data": value}), 200

@app.route('/persistence/getv2', methods=["POST"])
@app.route('/persistence/getV2', methods=["POST"])
@app.route('/persistence/getSortedValues', methods=["POST"])
def getVersion2():
    form_data = request.form

    return_data = []
    for starting_count in itertools.count(0):
        prefix = "qkeys[%d]" % starting_count
        scope = form_data.get(
            f"{prefix}.scope",
            'global',
        )

        target = form_data.get(
            f"{prefix}.target",
            None,
        )
        if target is None:
            break

        key = form_data.get(
            f"{prefix}.key",
            None,
        )
        if key is None:
            break

        result = DataStore.getData(scope, target, key)

        return_data.append({
            "Value": json.dumps(result),
            "Scope": scope,
            "Key": key,
            "Target": target,
        })

    if starting_count == 0:
        return jsonify({"data": [], "message": "No data being requested"}), 200
    
    return jsonify({"data": return_data}), 200
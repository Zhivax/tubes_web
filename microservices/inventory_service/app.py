from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock inventory database
inventory = {}

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)

@app.route('/inventory/<item_id>', methods=['GET', 'POST'])
def manage_inventory(item_id):
    if request.method == 'POST':
        inventory[item_id] = request.json
        return jsonify({"msg": "Item updated"}), 200
    return jsonify(inventory.get(item_id, {}))

if __name__ == '__main__':
    app.run(port=5002)

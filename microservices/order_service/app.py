from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock orders database
orders = {}

@app.route('/orders', methods=['GET', 'POST'])
def manage_orders():
    if request.method == 'POST':
        order = request.json
        order_id = len(orders) + 1
        orders[order_id] = order
        return jsonify({"order_id": order_id}), 201
    return jsonify(orders)

@app.route('/orders/<order_id>')
def get_order(order_id):
    return jsonify(orders.get(int(order_id), {}))

if __name__ == '__main__':
    app.run(port=5003)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/analytics/sales')
def sales_analytics():
    return jsonify({
        "daily_sales": 1000,
        "weekly_sales": 7000,
        "monthly_sales": 30000
    })

@app.route('/analytics/inventory')
def inventory_analytics():
    return jsonify({
        "total_items": 100,
        "low_stock_items": 5,
        "out_of_stock": 2
    })

if __name__ == '__main__':
    app.run(port=5005)

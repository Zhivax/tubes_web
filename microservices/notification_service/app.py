from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def send_notification():
    notification = request.json
    # Mock notification sending
    print(f"Sending notification: {notification}")
    return jsonify({"msg": "Notification sent"}), 200

@app.route('/notify/status/<notification_id>')
def get_notification_status(notification_id):
    return jsonify({"status": "delivered"})

if __name__ == '__main__':
    app.run(port=5004)

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Mock audit log storage
audit_logs = []

@app.route('/audit/log', methods=['POST'])
def log_action():
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': request.json.get('action'),
        'user_id': request.json.get('user_id'),
        'details': request.json.get('details')
    }
    audit_logs.append(log_entry)
    return jsonify({"msg": "Action logged"}), 201

@app.route('/audit/logs')
def get_logs():
    return jsonify(audit_logs)

if __name__ == '__main__':
    app.run(port=5007)

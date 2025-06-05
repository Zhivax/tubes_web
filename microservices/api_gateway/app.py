from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ROUTES = {
    'auth': 'http://localhost:5001',
    'inventory': 'http://localhost:5002',
    'orders': 'http://localhost:5003',
    'notifications': 'http://localhost:5004',
    'analytics': 'http://localhost:5005',
    'media': 'http://localhost:5006',
    'audit': 'http://localhost:5007',
    'search': 'http://localhost:5008'
}

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service, path):
    if service not in ROUTES:
        return jsonify({"error": "Service not found"}), 404

    url = f"{ROUTES[service]}/{path}"
    resp = requests.request(
        method=request.method,
        url=url,
        json=request.get_json() if request.is_json else None,
        headers=request.headers
    )
    
    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(port=5000)

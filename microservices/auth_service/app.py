from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
jwt = JWTManager(app)

@app.route('/auth/login', methods=['POST'])
def login():
    # Mock login - replace with actual DB logic
    if request.json.get('username') == 'admin' and request.json.get('password') == 'password':
        access_token = create_access_token(
            identity=request.json.get('username'),
            expires_delta=timedelta(days=1)
        )
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/auth/register', methods=['POST'])
def register():
    # Mock registration - replace with actual DB logic
    return jsonify({"msg": "User registered successfully"}), 201

if __name__ == '__main__':
    app.run(port=5001)

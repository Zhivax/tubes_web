import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables from .env (assume .env is one level up from this file)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

from controllers.auth_controller import auth_bp

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Register blueprint
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(port=5001, host='0.0.0.0', debug=True)

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Allow OAuth2 over HTTP for local dev

from flask import Flask, request, jsonify, redirect
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
import boto3
from botocore.exceptions import ClientError
import requests
from oauthlib.oauth2 import WebApplicationClient
from dotenv import load_dotenv

# Load environment variables from .env (assume .env is one level up from this file)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Google OAuth2 config
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = os.environ.get(
    "GOOGLE_DISCOVERY_URL",
    "https://accounts.google.com/.well-known/openid-configuration"
)

# DynamoDB config
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "users")
AWS_REGION = os.environ.get("AWS_REGION", "ap-southeast-1")
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
user_table = dynamodb.Table(DYNAMODB_TABLE)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/auth/login/google")
def login_google():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    # Use http for local redirect_uri
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/auth/login/google/callback")
def callback_google():
    code = request.args.get("code")
    if not code:
        return jsonify({"msg": "Missing code parameter in response. Did you approve the Google login?", "error": "missing_code"}), 400
    try:
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )
        client.parse_request_body_response(token_response.text)
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        userinfo = userinfo_response.json()
        if userinfo.get("email_verified"):
            unique_id = userinfo["sub"]
            users_email = userinfo["email"]
            users_name = userinfo["name"]

            try:
                user_table.put_item(
                    Item={
                        "user_id": unique_id,
                        "email": users_email,
                        "name": users_name,
                    },
                    ConditionExpression="attribute_not_exists(user_id)"
                )
            except ClientError as e:
                if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                    return jsonify({"msg": "Database error", "error": str(e)}), 500

            # Create JWT token
            access_token = create_access_token(
                identity=unique_id,
                expires_delta=timedelta(days=1)
            )
            return jsonify(access_token=access_token, email=users_email, name=users_name), 200
        else:
            return jsonify({"msg": "User email not available or not verified by Google."}), 400
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"msg": "Internal server error", "error": str(e)}), 500

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    if not data.get("email") or not data.get("user_id"):
        return jsonify({"msg": "Missing email or user_id"}), 400
    try:
        user_table.put_item(
            Item={
                "user_id": data["user_id"],
                "email": data["email"],
                "name": data.get("name", ""),
            },
            ConditionExpression="attribute_not_exists(user_id)"
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return jsonify({"msg": "User already exists"}), 409
        return jsonify({"msg": "Database error"}), 500
    return jsonify({"msg": "User registered successfully"}), 201

if __name__ == '__main__':
    app.run(port=5001, debug=True)

from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from botocore.exceptions import ClientError
import os

from utils.google_oauth import get_google_provider_cfg, client
from db.dynamodb import user_table

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/auth/login/google")
def login_google():
    session.clear()
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
        prompt="select_account"
    )
    return jsonify({"auth_url": request_uri})

@auth_bp.route("/auth/login/google/callback")
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
        import requests
        GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
        GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
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

            access_token = create_access_token(
                identity=unique_id,
                expires_delta=timedelta(days=1)
            )
            return jsonify({
                "access_token": access_token,
                "name": users_name,
                "email": users_email
            })
        else:
            return jsonify({"msg": "Email not verified", "error": "email_not_verified"}), 400
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"msg": "Server error", "error": "server_error"}), 500

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    if not data.get("email") or not data.get("user_id"):
        return jsonify({"msg": "Missing email or user_id"}), 400
    if "@" not in data["email"]:
        return jsonify({"msg": "Invalid email format"}), 400

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

@auth_bp.route('/auth/check', methods=['GET'])
@jwt_required()
def check_login():
    user_id = get_jwt_identity()
    return jsonify({"msg": "Token valid", "user_id": user_id}), 200

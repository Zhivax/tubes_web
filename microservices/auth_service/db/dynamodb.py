import os
import boto3

DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "users")
AWS_REGION = os.environ.get("AWS_REGION", "ap-southeast-1")
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
user_table = dynamodb.Table(DYNAMODB_TABLE)

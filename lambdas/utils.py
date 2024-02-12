import json
import os
import boto3
from opensearchpy import OpenSearch


# Env params
os_secret = os.environ.get("OPEN_SEARCH_SECRET")
os_domain_endpoint = os.environ.get("OPEN_SEARCH_DOMAIN_ENDPOINT")

# Initialization
sm_client = boto3.client("secretsmanager")
sm_response = sm_client.get_secret_value(SecretId=os_secret)
secret = json.loads(sm_response["SecretString"])
auth_pass = (secret.get("username"), secret.get("password"))
os_domain_port = {"host": os_domain_endpoint, "port": 443}

os_client = OpenSearch(
    hosts=[os_domain_port],
    http_compress=True,
    http_auth=auth_pass,
    use_ssl=True,
    verify_certs=True,
)


# Util functions
def check_index_exists(index_name):
    if not os_client.indices.exists(index=index_name):
        raise IndexNotFoundException("Invalid parameter!")

def get_response(status=400, message="", data=None):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
    }
    return {
        "statusCode": status,
        "headers": headers,
        "body": json.dumps({"message": message, "data": data}, default=str),
    }


# Exceptions
class ValidationError(Exception):
    pass

class IndexNotFoundException(Exception):
    pass


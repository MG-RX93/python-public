import os
import requests
from dotenv import load_dotenv  # pip install python-dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Globals for caching
_cached_token = None
_token_expiry = datetime.now()
_instance_url = None


def get_access_token():
    global _cached_token, _token_expiry, _instance_url

    # Check if the cached token is still valid
    if _cached_token and datetime.now() < _token_expiry:
        return _cached_token, _instance_url  # Placeholder for instance URL

    # Salesforce OAuth endpoints
    auth_url = os.getenv("SF_AUTH_URL")

    # Use environment variables
    client_id = os.getenv("SF_CONSUMER_KEY")
    client_secret = os.getenv("SF_CONSUMER_SECRET")
    username = os.getenv("SF_USERNAME")
    password = os.getenv("SF_PASSWORD")
    token_lifetime = int(os.getenv("SF_TOKEN_LIFETIME"))

    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
    }

    response = requests.post(auth_url, data=data)
    auth_response = response.json()

    _cached_token = auth_response["access_token"]
    _instance_url = auth_response["instance_url"]
    # Use issued_at to calculate the expiry time, assuming a default lifetime (e.g., 1 hour)
    issued_at = datetime.fromtimestamp(int(auth_response["issued_at"]) / 1000)
    # Assuming a token lifetime of 1 hour (3600 seconds)
    _token_expiry = issued_at + timedelta(seconds=token_lifetime)

    return _cached_token, auth_response["instance_url"]

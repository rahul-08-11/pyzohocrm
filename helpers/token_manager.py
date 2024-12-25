from datetime import datetime, timedelta
import requests
import os
import json
class TokenManager:
    _token = None
    _expiry = None

    def get_access_token(cls):
        if os.path.exists("token.json"):
            pass

        else:
            with open("token.json","w") as f:
                cls.refresh_token()
                f.write(json.dumps({"token": cls._token, "expiry": cls._expiry.strftime("%Y-%m-%d %H:%M:%S")}))

        if cls._token is None or cls.is_token_expired():
            cls.refresh_token()
        return cls._token

    def is_token_expired(cls):
        # Assuming the token is valid for 50 minutes
        return cls._expiry is None or datetime.now() >= cls._expiry

    def refresh_token(cls):
        # Call the Zoho API to refresh the token
        url = "https://accounts.zohocloud.ca/oauth/v2/token"
        ## prepare the parameters
        params = {
            "refresh_token": os.getenv("REFRESH_TOKEN"),
            "client_id": os.getenv("CLIENT_ZOHO_ID"),
            "client_secret": os.getenv("CLIENT_ZOHO_SECRET"),
            "grant_type": "refresh_token",
        }
        ## send post request
        response = requests.post(url, params=params)

        if response.status_code == 200:
            cls._expiry = datetime.now() + timedelta(minutes=50)  # Update expiry time
            print("expirey time is set", cls._expiry)
            cls._token = response.json()["access_token"]

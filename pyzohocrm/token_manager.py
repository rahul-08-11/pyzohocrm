#pyzohobook/token_manager.py

import json
import requests
from datetime import datetime, timedelta
import os


class TokenManager:
    """
    A class for managing Zoho Books API tokens.

    Attributes:
        _token (str): The current access token.
        _expiry (datetime): The expiration time of the current access token.

    Methods:
        _refresh_token(): Refreshes the access token by calling the Zoho API.

        _is_token_expired(): Checks if the current access token is expired.

        _get_access_token(): Retrieves the current access token.

        _get_domain_url(): Retrieves the domain URL based on the domain name.

    Instance Variables:
        domain_url (str): The base URL for the Zoho Books API.
        refresh_token (str): The refresh token for the Zoho Books API.
        client_id (str): The client ID for the Zoho Books API.
        client_secret (str): The client secret for the Zoho Books API.
        grant_type (str): The grant type for the Zoho Books API.

    """
    _token = None
    _expiry = None

    def __init__(self, domain_name : str, refresh_token : str, client_id : str, client_secret : str, grant_type : str, token_dir : str = "./", token_filename : str = "token.json") -> None:
        self.domain_url = self._get_domain_url(domain_name.lower())
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.token_path = os.path.join(token_dir, token_filename)

    def _get_domain_url(self, domain_name) -> str:
        zoho_urls = {
            "united states": "https://accounts.zoho.com/",
            "europe": "https://accounts.zoho.eu/",
            "india": "https://accounts.zoho.in/",
            "australia": "https://accounts.zoho.com.au/",
            "japan": "https://accounts.zoho.jp/",
            "canada": "https://accounts.zohocloud.ca/",
        }
        return zoho_urls[domain_name]

    def get_access_token(self) -> str:
        # store at project level
        if os.path.exists(self.token_path):
            pass

        else:
            with open(self.token_path, "w") as f:
                self._refresh_token()
                f.write(
                    json.dumps(
                        {
                            "token": self._token,
                            "expiry": self._expiry.strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
                )

        if self._token is None or self._is_token_expired():
            self._refresh_token()
        return self._token

    def _is_token_expired(self) -> bool:
        # Assuming the token is valid for 50 minutes
        return self._expiry is None or datetime.now() >= self._expiry

    def _refresh_token(self) -> None:
        # Call the Zoho API to refresh the token
        url = f"{self.domain_url}oauth/v2/token"
     
        ## prepare the parameters
        params = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
        }
        ## send post request
        response = requests.post(url, params=params)
        if response.status_code == 200:
            self._expiry = datetime.now() + timedelta(minutes=50)  # Update expiry time
            self._token = response.json()["access_token"]



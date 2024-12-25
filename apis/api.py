import os
import logging
import aiohttp
from helpers import TokenManager
from typing import Literal
import os
import requests


class ZOHOAPI(TokenManager):
    def __init__(self):
        # Initialize the base class Methods
        super().__init__()
        self.base_url = os.getenv("ZOHO_BASE_URL")
        self.payload = {"data": []}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def _get_headers(self):
        return {
            "Authorization": f"Zoho-oauthtoken {self.get_access_token()}",
            "Content-Type": "application/json"
        }

    async def _make_async_request(self, method : Literal["GET", "POST", "PUT", "DELETE","PATCH"], url : str, data : str):
        try:
            with aiohttp.ClientSession() as session:
                with session.request(method, url, headers=self._get_headers(), json=data) as response:
                    return response.json()  # Return JSON content
        except aiohttp.ClientError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise


    def _make_request(self, method : Literal["GET", "POST", "PUT", "DELETE","PATCH"], url : str, data : str):
        try:
            
            response = requests.Request(method, url, headers=self._get_headers(), json=data)
            return response

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

        
    # Basic CRUD operations
    def create(self, moduleName: str, data: dict):
        url = f"{self.base_url}/{moduleName}"
        return self._make_request("POST", url, json=data)

    def read(self, moduleName: str, id: str = None):
        url = f"{self.base_url}/{moduleName}"
        if id:
            url += f"/{id}"
        return self._make_request("GET", url)

    def update(self, moduleName: str, id: str, data: dict):
        url = f"{self.base_url}/{moduleName}/{id}"
        return self._make_request("PUT", url, json=data)

    def partial_update(self, moduleName: str, id: str, data: dict):
        url = f"{self.base_url}/{moduleName}/{id}"
        return self._make_request("PATCH", url, data={"data":[data]})

    def delete(self, moduleName: str, id: str):
        url = f"{self.base_url}/{moduleName}/{id}"
        return self._make_request("DELETE", url)

    # Advanced operations
    def attach_file(self, moduleName: str, id: str, file_path: str = None, file_url: str = None):
        url = f"{self.base_url}/{moduleName}/{id}/Attachments"
        data = {}

        if file_path:
            # Use `with` to ensure file is properly closed
            with open(file_path, "rb") as f:
                files = {"file": f}
                data = {}
                return self._make_request("POST", url, data=data, files=files)

        elif file_url:
            data["attachmentUrl"] = file_url
            return self._make_request("POST", url, data=data)

        else:
            raise ValueError("Either file_path or file_url must be provided.")

    def fetch_file(self, moduleName: str, id: str = None, file_id: str = None):
        if file_id:
            url = f"{self.base_url}/{moduleName}/{id}/Attachments/{file_id}"
            return self._make_request("GET", url)
        elif id:
            url = f"{self.base_url}/{moduleName}/{id}/Attachments"
            return self._make_request("GET", url)
        else:
            raise ValueError("Either file_id or id must be provided.")

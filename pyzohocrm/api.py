import os
import logging
import requests
from typing import Literal
from .utils import *

class ZohoApi():
    """
    A utility class to interact with the Zoho CRM API. This class provides methods to perform CRUD operations
    and manage attachments for Zoho CRM modules.

    Attributes:
        base_url (str): The base URL for the Zoho CRM API.
        logger (logging.Logger): Logger instance for logging API events and errors.
    """

    def __init__(self, base_url: str) -> None:
        """
        Initializes the ZohoApi class with the given base URL.

        Args:
            base_url (str): The base URL of the Zoho CRM API.
        """
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def _make_request(self, method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"], url: str, json=None,data=None, files=None, token=None) -> requests.Response:
        """
        Makes an HTTP request to the Zoho CRM API.

        Args:
            method (Literal): The HTTP method (e.g., GET, POST, PUT, DELETE, PATCH).
            url (str): The full API endpoint URL.
            data (dict, optional): The JSON payload for the request.
            files (dict, optional): Files to be uploaded.
            token (str, optional): Authorization token.

        Returns:
            requests.Response: The response object from the API request.

        Raises:
            requests.RequestException: If an HTTP error occurs.
            Exception: For any unexpected errors.
        """
        try:
            response = requests.request(method, url, headers=get_header(token=token), json=json, data=data, files=files)
            # response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

    def create_record(self, moduleName: str, data: dict, token: str = None) -> requests.Response:
        """
        Creates a new record in the specified Zoho CRM module.

        Args:
            moduleName (str): The name of the Zoho CRM module.
            data (dict): The record data to be created.
            token (str, optional): Authorization token.

        Returns:
            requests.Response: The response object.
        """
        url = f"{self.base_url}/{moduleName}"
        return self._make_request("POST", url, json=data, token=token)

    def read_record(self, moduleName: str, id: str = None, token: str = None) -> requests.Response:
        """
        Reads records or a specific record from the specified Zoho CRM module.

        Args:
            moduleName (str): The name of the Zoho CRM module.
            id (str, optional): The record ID. If None, fetches all records.
            token (str, optional): Authorization token.

        Returns:
            requests.Response: The response object.
        """
        url = f"{self.base_url}/{moduleName}"
        if id:
            url += f"/{id}"
        return self._make_request("GET", url, token=token)

    def fetch_module_data(self, moduleName: str, token: str = None) -> requests.Response:
        """
        Fetches data from a specified module.

        Args:
            moduleName (str): The name of the Zoho CRM module.
            token (str, optional): Authorization token.

        Returns:
            requests.Response: The response object.
        """
        url = f"{self.base_url}/{moduleName}"
        return self._make_request("GET", url, token=token)

    def update_record(self, moduleName: str, id: str, data: dict, token: str = None) -> requests.Response:
        """
        Updates a specific record in the specified Zoho CRM module.

        Args:
            moduleName (str): The name of the Zoho CRM module.
            id (str): The record ID to update.
            data (dict): The updated record data.
            token (str, optional): Authorization token.

        Returns:
            requests.Response: The response object.
        """
        url = f"{self.base_url}/{moduleName}/{id}"
        return self._make_request("PUT", url, json=data, token=token)

    def patch_record(self, moduleName: str, id: str, data: dict, token: str = None) -> requests.Response:
        """
        Partially updates a specific record in the specified Zoho CRM module.

        Args:
            moduleName (str): The name of the Zoho CRM module.
            id (str): The record ID to update.
            data (dict): The data to update.
            token (str, optional): Authorization token.

        Returns:
            requests.Response: The response object.
        """
        url = f"{self.base_url}/{moduleName}/{id}"
        return self._make_request("PATCH", url, json={"data": [data]}, token=token)

    def delete_record(self, moduleName: str, id: str, token: str = None) -> requests.Response:
        """
        Deletes a specific record in the specified Zoho CRM module.

        Args:
            moduleName (str): The name of the Zoho CRM module.
            id (str): The record ID to delete.
            token (str, optional): Authorization token.

        Returns:
            requests.Response: The response object.
        """
        url = f"{self.base_url}/{moduleName}/{id}"
        return self._make_request("DELETE", url, token=token)

    def attach_file(self, moduleName: str, record_id: str, file_path: str = None, file_url: str = None, token: str = None) -> requests.Response:
        """
        Attaches a file to a specific record in the specified Zoho CRM module.

        Args:
            moduleName (str): The name of the Zoho CRM module.
            id (str): The record ID to attach the file to.
            file_path (str, optional): The path to the local file to attach.
            file_url (str, optional): The URL of the file to attach.
            token (str, optional): Authorization token.

        Returns:
            requests.Response: The response object.

        Raises:
            ValueError: If neither file_path nor file_url is provided.
        """
        url = f"{self.base_url}/{moduleName}/{record_id}/Attachments"
        
        if file_path:
            with open(file_path, "rb") as f:
                files = {"file": f}
                return self._make_request("POST", url, files=files, token=token)
        elif file_url:
            data = {"attachmentUrl": file_url}
            return self._make_request("POST", url, data=data, token=token)
        else:
            raise ValueError("Either file_path or file_url must be provided.")

    def fetch_file(self, moduleName: str, record_id: str, file_id: str = None, token: str = None, fetch_all: bool = True) -> requests.Response:
        """
        Fetches file attachments from a specific record in the specified Zoho CRM module.

        This function allows you to:
        - Fetch all attachments associated with a specific record, by setting `fetch_all=True` (default behavior).
        - Fetch a specific file attachment from a record, by providing both `record_id` and `file_id` and setting `fetch_all=False`.

        Args:
            moduleName (str): The name of the Zoho CRM module.
            record_id (str): The record ID for which attachments are to be fetched. This is a required argument.
            file_id (str, optional): The specific file ID to fetch. Required if `fetch_all` is set to False.
            token (str, optional): Authorization token.
            fetch_all (bool, optional): If True, fetch all attachments for the given record. If False, fetch a specific file attachment. Defaults to True.

        Returns:
            requests.Response: The response object containing the attachment(s).

        Raises:
            ValueError: If `file_id` is not provided when `fetch_all` is False, or if `record_id` is not provided.

        Example:
            - To fetch all attachments for a specific record:
                fetch_file('Leads', '12345')
            - To fetch a specific file attachment for a record:
                fetch_file('Leads', '12345', file_id='67890', fetch_all=False)
        """
        if not record_id:
            raise ValueError("record_id is required.")
        
        if not token:
            raise ValueError("token is required.")

        if fetch_all:
            url = f"{self.base_url}/{moduleName}/{record_id}/Attachments"
        else:
            if not file_id:
                raise ValueError("file_id must be provided when fetch_all is False.")
            url = f"{self.base_url}/{moduleName}/{record_id}/Attachments/{file_id}"

        return self._make_request("GET", url, token=token)
    
    def fetch_related_list(self, moduleName: str, record_id: str, token: str, name : str) -> requests.Response:
        """
        Fetches related list data from a specific record in the specified Zoho CRM module.

        Args:
            moduleName (str): The name of the Zoho CRM module.
            record_id (str): The record ID for which related list data is to be fetched.
            token (str): Authorization token.
            name (str): The name of the related list to fetch.

        Returns:
            requests.Response: The response object containing the related list data.

        Raises:
            ValueError: If `record_id` is not provided, `token` is not provided, or `name` is not provided.

        """
        if not record_id:
            raise ValueError("record_id is required.")

        if not token:
            raise ValueError("token is required.")
        
        if not name:
            raise ValueError("name is required.")
        
        url = f"{self.base_url}/{moduleName}/{record_id}/{name}"

        return self._make_request("GET", url, token=token)
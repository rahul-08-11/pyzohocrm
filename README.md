# pyzohocrm - A Simplified Zoho CRM Python Client

pyzohocrm is a lightweight Python package designed for interacting with Zoho CRM. It provides a simpler and more intuitive alternative to the official Zoho Python SDK while including built-in token management for hassle-free authentication.

## Features

- Simplified CRUD operations for Zoho CRM modules.
- Easy handling of file attachments and downloads.
- Token management built-in for seamless API authentication.
- Flexible support for additional Zoho CRM API methods.

## Installation


Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the package directly from your Git repository using pip:

```bash
pip install git+https://github.com/rahul-08-11/pyzohocrm.git
```

## Usage

### Importing and Initializing

```python
from your_package_name.zoho_api import ZOHOAPI

# Initialize with your Zoho CRM base URL
api = ZOHOAPI(base_url="https://www.zohoapis.com/crm/v2")
```

### Example Operations

#### Create a Record
```python
response = api.create(moduleName="Leads", data={"Company": "Acme Corp", "Last_Name": "Doe"}, token="your_access_token")
print(response.json())
```

#### Read Records
```python
response = api.read(moduleName="Leads", token="your_access_token")
print(response.json())
```

#### Update a Record
```python
response = api.update(moduleName="Leads", id="record_id", data={"Last_Name": "Smith"}, token="your_access_token")
print(response.json())
```

#### Attach a File
```python
response = api.attach_file(moduleName="Leads", id="record_id", file_path="/path/to/file.pdf", token="your_access_token")
print(response.json())
```

#### Fetch a File
```python
response = api.fetch_file(moduleName="Leads", record_id="record_id", file_id="file_id", token="your_access_token")
with open("downloaded_file.pdf", "wb") as file:
    file.write(response.content)
```

## Token Management

This package includes built-in support for managing tokens. Use the `get_header()` utility to generate headers with the correct authorization token.

### Example

```python
from your_package_name.utils import get_header

headers = get_header(token="your_access_token")
print(headers)
```

## Logging

ZOHOAPI uses Python's built-in `logging` module to log errors and API events. Customize logging levels as needed for your application.

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Contributing

Feel free to contribute by submitting issues or pull requests in the Git repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

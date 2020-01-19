# Dome9 SDK python

Author - Dome9 SRE Team [mail_us](mailto:d9ops@checkpoint.com)

This SDK implements a Python wrapper for the Dome9 API V2.

For official Dome9 API documentation please refer to https://api-v2-docs.dome9.com/

Quick Start
-----------

Installation
~~~~~~~~~~~~

$ pip install git+https://github.com/dome9/dome9-sdk-python


Usage example - Role
~~~~~~~~~~~~
```python
from dome9_type_annotations.client import Client
from resources.role import CreateRole


dome9_client = Client(access_id='ACCESS_ID', secret_key='SECRET_KEY')
payload = CreateRole(name='my-role', description='my-description')
response = dome9_client.role.create(body=payload)

print(response)
```
# Dome9 SDK python

Author - Dome9 SRE Team [mail_us](mailto:d9ops@checkpoint.com)

This SDK implements a Python wrapper for the Dome9 API V2.

Dome9 API documentation: https://api-v2-docs.dome9.com/

Quick Start
-----

### Installation
```bash
$ pip install git+https://github.com/dome9/dome9-sdk-python
```

### Import
Client can be imported from dome9_type_annotations layer to support IDE methods completion
```python
from dome9_type_annotations.client import Client
```
Client can also be imported directly 
```python
from dome9 import Client
```

### Client Init

Required parameters for client initiation (`access_id`, `secret_key`) can be passed directly:
```python
dome9_client = Client(access_id='ACCESS_ID', secret_key='SECRET_KEY')
```

Alternatively, If parameters are not provided, `Client` will seek and use `DOME9_ACCESS_ID` and `DOME9_SECRET_KEY` **environment variables**
```python
dome9_client = Client()
``` 

By default, client will use Dome9 production URL `https://api.dome9.com/v2/`. For development purposes, different URL can be provided

### Example - Create Role
```python
from dome9_type_annotations.client import Client
from resources.role import CreateRole

dome9_client = Client(access_id='ACCESS_ID', secret_key='SECRET_KEY')
payload = CreateRole(name='my-role', description='my-description')
response = dome9_client.role.create(body=payload)

print(response)
```
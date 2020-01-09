from dataclasses import dataclass
from enum import Enum

from loguru import logger
from dome9.client import Client
from dome9.base_dataclass import BaseDataclassRequest

from dome9.resource import Dome9Resource


class AzureCloudAccountConsts(Enum):
	MAIN_ROUTE = 'AzureCloudAccount'
	OPERATION_MODE_ROUTE = 'OperationMode'
	ORGANIZATIONAL_UNIT_ROUTE = 'organizationalUnit'
	NAME_ROUTE = 'AccountName'
	CREDENTIALS_ROUTE = 'credentials'

class AzureCloudAccountOperationModeConsts(Enum):
	READ_ONLY = 'Read'
	MANAGED = 'Manage'


@dataclass
class AzureCloudAccountCredentials(BaseDataclassRequest):
	"""Azure cloud account credentials

		Args:
			client_id (str): (Required) Azure account id
			client_password (str): (Required) Password for account

	"""

	client_id: str
	client_password: str


@dataclass
class AzureCloudAccountRequest(BaseDataclassRequest):
	"""Azure cloud account request

		Args:
			name (str): (Required) The name of the Azure account in Dome9
			subscription_id (str): (Required) The Azure subscription id for account
			tenant_id (str): (Required) The Azure tenant id
			credentials (stAzureCloudAccountCredentials): (Required) Credentials
			operation_mode (str): (Required) Dome9 operation mode for the Azure account ("Read-Only" or "Managed")
			organizational_unit_id (str): (Optional) Organizational Unit that this cloud account will be attached to

	"""

	name: str
	subscription_id: str
	tenant_id: str
	credentials: AzureCloudAccountCredentials
	operation_mode: str
	organizational_unit_id: str = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		operation_mode_options = [operation_mode_option.value for operation_mode_option in AzureCloudAccountOperationModeConsts]
		if self.operation_mode not in operation_mode_options:
			raise ValueError(f'operation mode must be one of the following {operation_mode_options}')


@dataclass
class AzureCloudAccountUpdateName(BaseDataclassRequest):
	"""Azure cloud account update name

		Args:
			name (str): (Required) The desired name for Azure cloud account
	"""

	name: str


@dataclass
class AzureCloudAccountUpdateOperationMode(BaseDataclassRequest):
	"""Azure cloud account update name

		Args:
			operation_mode (str): Dome9 operation mode for the Azure account ("Read-Only" or "Managed")
	"""

	operation_mode: str

	@logger.catch(reraise=True)
	def __post_init__(self):
		operation_mode_options = [operation_mode_option.value for operation_mode_option in AzureCloudAccountOperationModeConsts]
		if self.operationMode not in operation_mode_options:
			raise ValueError(f'operation mode must be one of the following {operation_mode_options}')


@dataclass
class AzureCloudAccountUpdateOrganizationalUnitID(BaseDataclassRequest):
	"""Azure cloud account update name

		Args:
			organizational_unit_id (str): (Required) Organizational Unit ID
	"""

	organizational_unit_id: str


@dataclass
class AzureCloudAccountUpdateCredentials(BaseDataclassRequest):
	"""Azure cloud account update credentials

		Args:
			application_id (str): (Required) Azure application ID
			application_key (str): (Required) Azure application key
	"""

	application_id: str
	application_key: str


class AzureCloudAccount(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: AzureCloudAccountRequest):
		return self._post(route=AzureCloudAccountConsts.MAIN_ROUTE.value, body=body)

	def get(self, azure_cloud_account_id: str):
		route = f'{AzureCloudAccountConsts.MAIN_ROUTE.value}/{azure_cloud_account_id}'
		return self._get(route=route)

	def get_all(self):
		return self._get(route=AzureCloudAccountConsts.MAIN_ROUTE.value)

	def update_name(self, azure_cloud_account_id: str, body: AzureCloudAccountUpdateName):
		route = f'{AzureCloudAccountConsts.MAIN_ROUTE.value}/{azure_cloud_account_id}/{AzureCloudAccountConsts.NAME_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_operation_mode(self, azure_cloud_account_id: str, body: AzureCloudAccountUpdateOperationMode):
		route = f'{AzureCloudAccountConsts.MAIN_ROUTE.value}/{azure_cloud_account_id}/{AzureCloudAccountConsts.OPERATION_MODE_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_credentials(self, azure_cloud_account_id: str, body: AzureCloudAccountUpdateCredentials):
		route = f'{AzureCloudAccountConsts.MAIN_ROUTE.value}/{azure_cloud_account_id}/{AzureCloudAccountConsts.CREDENTIALS_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_organizational_id(self, azure_cloud_account_id: str, body: AzureCloudAccountUpdateOrganizationalUnitID):
		route = f'{AzureCloudAccountConsts.MAIN_ROUTE.value}/{azure_cloud_account_id}/{AzureCloudAccountConsts.ORGANIZATIONAL_UNIT_ROUTE.value}'
		return self._put(route=route, body=body)

	def delete(self, azure_cloud_account_id: str):
		route = f'{AzureCloudAccountConsts.MAIN_ROUTE.value}/{azure_cloud_account_id}'
		return self._delete(route=route)
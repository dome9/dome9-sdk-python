from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union

from loguru import logger
from dome9 import Client, BaseDataclassRequest, Dome9Resource


class AzureCloudAccountConsts(Enum):
	AZURE_CLOUD_ACCOUNT = 'AzureCloudAccount'
	OPERATION_MODE = 'OperationMode'
	ORGANIZATIONAL_UNIT = 'organizationalUnit'
	ACCOUNT_NAME = 'AccountName'
	CREDENTIALS = 'credentials'


class AzureCloudAccountOperationModeConsts(Enum):
	READ_ONLY = 'Read'
	MANAGED = 'Manage'


@dataclass
class AzureAccountCredentials(BaseDataclassRequest):
	"""Azure cloud account credentials

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azureaccountcredentialsviewmodel
	:param client_id: Azure account id
	:type  client_id: str
	:param client_password: Password for account
	:type  client_password: str

	"""
	client_id: str
	client_password: str


@dataclass
class AzureCloudAccountRequest(BaseDataclassRequest):
	"""Azure cloud account request

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
	:param name: account name (in Dome9)
	:type  name: str
	:param subscription_id: Azure subscription id for account
	:type  subscription_id: str
	:param tenant_id: Azure tenant id
	:type  tenant_id: str
	:param credentials: Azure account credentials
	:type  credentials: AzureAccountCredentials
	:param operation_mode: Dome9 operation mode for the Azure account (Read-Only or Managed)
	:type  operation_mode: str
	:param organizational_unit_id:
	:type  organizational_unit_id: str

	"""
	name: str
	subscription_id: str
	tenant_id: str
	credentials: AzureAccountCredentials
	operation_mode: str
	organizational_unit_id: str = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		operation_mode_options = [operation_mode_option.value for operation_mode_option in AzureCloudAccountOperationModeConsts]
		if self.operation_mode not in operation_mode_options:
			raise ValueError(f'operation mode must be one of the following {operation_mode_options}')


@dataclass
class AzureAccountNameMode(BaseDataclassRequest):
	"""

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-azure-accounts-azureaccountnamemodeviewmodel
	:param name:
	:type  name: str

	"""
	name: str


@dataclass
class AzureAccountOperationMode(BaseDataclassRequest):
	"""

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-azure-accounts-azureaccountoperationmodeviewmodel
	:param operation_mode:
	:type  operation_mode: str

	"""
	operation_mode: str

	@logger.catch(reraise=True)
	def __post_init__(self):
		operation_mode_options = [operation_mode_option.value for operation_mode_option in AzureCloudAccountOperationModeConsts]
		if self.operationMode not in operation_mode_options:
			raise ValueError(f'operation mode must be one of the following {operation_mode_options}')


@dataclass
class AzureCloudAccountUpdateOrganizationalUnitID(BaseDataclassRequest):
	"""

	:link
	:param organizational_unit_id:
	:type  organizational_unit_id: str

	"""
	organizational_unit_id: str


@dataclass
class AzureCloudAccountCredentialsPut(BaseDataclassRequest):
	"""

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-azure-accounts-azurecloudaccountcredentialsputviewmodel
	:param application_id:
	:type  application_id: str
	:param application_key:
	:type  application_key: str

	"""
	application_id: str
	application_key: str


class AzureCloudAccount(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: AzureCloudAccountRequest) -> Dict:
		"""Add (onboard) an Azure account to the user's Dome9 account

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_post
		:param   body: details for the Azure account
		:type    body: AzureCloudAccountRequest
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		return self._post(route=AzureCloudAccountConsts.AZURE_CLOUD_ACCOUNT.value, body=body)

	def get(self, azure_cloud_account_id: str = '') -> Union[List[Dict], Dict]:
		"""Get details for all Azure accounts for the Dome9 user

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_get
		:param   azure_cloud_account_id:
		:type    azure_cloud_account_id: str
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		route = f'{AzureCloudAccountConsts.AZURE_CLOUD_ACCOUNT.value}/{azure_cloud_account_id}'
		return self._get(route=route)

	def update_account_name(self, azure_cloud_account_id: str, body: AzureAccountNameMode) -> Dict:
		"""Update the account name (in Dome9) for an Azure account

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_updateaccountname
		:param   azure_cloud_account_id: the account id in Dome9
		:type    azure_cloud_account_id: str
		:param   body: the new name for the account
		:type    body: AzureAccountNameMode
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		route = f'{AzureCloudAccountConsts.AZURE_CLOUD_ACCOUNT.value}/{azure_cloud_account_id}/{AzureCloudAccountConsts.ACCOUNT_NAME.value}'
		return self._put(route=route, body=body)

	def update_operation_mode(self, azure_cloud_account_id: str, body: AzureAccountOperationMode) -> Dict:
		"""Update the operations mode for an Azure account in Dome9. Modes can be Read-Only or Manage

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_updateoperationmodeasync
		:param   azure_cloud_account_id: the account id for the Azure account in Dome9
		:type    azure_cloud_account_id: str
		:param   body: updated details for the account, including the operations mode
		:type    body: AzureAccountOperationMode
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		route = f'{AzureCloudAccountConsts.AZURE_CLOUD_ACCOUNT.value}/{azure_cloud_account_id}/{AzureCloudAccountConsts.OPERATION_MODE.value}'
		return self._put(route=route, body=body)

	def update_cloud_account_credentials(self, azure_cloud_account_id: str, body: AzureCloudAccountCredentialsPut) -> Dict:
		"""

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_updatecloudaccountcredentials
		:param   azure_cloud_account_id:
		:type    azure_cloud_account_id: str
		:param   body:
		:type    body: AzureCloudAccountCredentialsPut
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		route = f'{AzureCloudAccountConsts.AZURE_CLOUD_ACCOUNT.value}/{azure_cloud_account_id}/{AzureCloudAccountConsts.CREDENTIALS.value}'
		return self._put(route=route, body=body)

	def update_organizational_id(self, azure_cloud_account_id: str, body: AzureCloudAccountUpdateOrganizationalUnitID) -> Dict:
		"""Update the ID of the Organizational Unit that this cloud account will be attached to. Use 'null' for th root organizational unit

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_updateorganziationalid
		:param   azure_cloud_account_id: The Dome9 Guid ID of the Azure cloud account
		:type    azure_cloud_account_id: str
		:param   body: The Guid ID of the Organizational Unit to attach to. Use 'null' to attach to the root Organizational Unit
		:type    body: AzureCloudAccountUpdateOrganizationalUnitID
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		route = f'{AzureCloudAccountConsts.AZURE_CLOUD_ACCOUNT.value}/{azure_cloud_account_id}/{AzureCloudAccountConsts.ORGANIZATIONAL_UNIT.value}'
		return self._put(route=route, body=body)

	def delete(self, azure_cloud_account_id: str) -> None:
		"""Delete an Azure account from a Dome9 account (the Azure account is not deleted from Azure)

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_delete
		:param   azure_cloud_account_id: the Dome9 account id for the account
		:type    azure_cloud_account_id: str
		:return: None

		"""
		route = f'{AzureCloudAccountConsts.AZURE_CLOUD_ACCOUNT.value}/{azure_cloud_account_id}'
		return self._delete(route=route)

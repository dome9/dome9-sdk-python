from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union

from dome9 import Client, BaseDataclassRequest, Dome9Resource


class GoogleCloudAccountConsts(Enum):
	"""
	GoogleCloudAccountConsts
	"""
	GOOGLE_CLOUD_ACCOUNT = 'GoogleCloudAccount'
	ACCOUNT_NAME_ROUTE = 'AccountName'
	CREDENTIALS = 'Credentials'
	GSUITE = 'Gsuite'
	ORGANIZATIONAL_UNIT_MOVE = 'organizationalUnit/move'


@dataclass
class GoogleAccountGsuite(BaseDataclassRequest):
	"""
	
	:link  https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googleaccountgsuiteviewmodel
	:param gsuite_user:
	:type  gsuite_user: str
	:param domain_name:
	:type  domain_name: Dict
	"""
	
	gsuite_user: str
	domain_name: str


@dataclass
class GoogleCloudAccountPost(BaseDataclassRequest):
	"""GoogleCloudAccountPost
	
	:link  https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googlecloudaccountpostviewmodel
	:param name: Google account name in Dome9
	:type  name: str
	:param service_account_credentials: The service account JSON block (from the GCP console)
	:type  service_account_credentials: Dict
	:param organizational_unit_id:
	:type  organizational_unit_id: str
	:param gsuite_user:
	:type  gsuite_user: str
	:param domain_name:
	:type  domain_name: str
	
	"""
	name: str
	service_account_credentials: Dict
	organizational_unit_id: str = None
	gsuite_user: str = None
	domain_name: str = None


@dataclass
class GoogleCloudAccountUpdate(BaseDataclassRequest):
	"""GoogleCloudAccountUpdate
	
	:link  https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googlecloudaccountupdateviewmodel
	:param name: Google account name in Dome9
	:type  name: str
	:param service_account_credentials: The service account JSON block (from the GCP console)
	:type  service_account_credentials: Dict
	
	"""
	name: str
	service_account_credentials: object


@dataclass
class GoogleAccountName(BaseDataclassRequest):
	"""GoogleAccountName
	
	:link  https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googleaccountnameviewmodel
	:param name: Google account name in Dome9
	:type  name: str
	
	"""
	name: str


@dataclass
class MoveOrganizationalUnit(BaseDataclassRequest):
	"""MoveOrganizationalUnit

	:link  https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-organizationalunit-moveorganizationalunitviewmodel
	:param source_organizational_unit_id:
	:type  source_organizational_unit_id: str
	:param target_organizational_unit_id:
	:type  target_organizational_unit_id: str

	"""
	source_organizational_unit_id: str
	target_organizational_unit_id: str


@dataclass
class GoogleCloudAccount(Dome9Resource):
	"""
	GoogleCloudAccount
	"""
	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: GoogleCloudAccountPost) -> Dict:
		"""Add (onboard) a new Google cloud account to Dome9

		:link    https://api-v2-docs.dome9.com/index.html#googlecloudaccount_post
		:param   body: details for the new account
		:type    body: GoogleCloudAccountRequest
		:return  https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googlecloudaccountgetviewmodel
		:rtype   GoogleAccountGsuite

		"""
		return self._post(route=GoogleCloudAccountConsts.GOOGLE_CLOUD_ACCOUNT.value, body=body)

	def get(self, google_cloud_account_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get details for a specific Google Cloud Account

		:link    https://api-v2-docs.dome9.com/index.html#googlecloudaccount_get
		:param   google_cloud_account_id: the Google cloud account id , if id is not provided will return all google accounts
		:type    google_cloud_account_id: str
		:return  https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googlecloudaccountgetviewmodel
		:rtype   GoogleCloudAccountGet

		"""
		route = f'{GoogleCloudAccountConsts.GOOGLE_CLOUD_ACCOUNT.value}/{google_cloud_account_id}'
		return self._get(route=route)

	def update_account_name(self, gcp_cloud_account_id: str, body: GoogleAccountName) -> Dict:
		"""Update a Google Cloud account name (as it appears in Dome9)

		:link:  https://api-v2-docs.dome9.com/index.html#googlecloudaccount_updateaccountname
		:param  gcp_cloud_account_id: the account id
		:type   gcp_cloud_account_id: str
		:param  body: the updated name as it will appear in Dome9
		:type   body: GoogleAccountName
		:return https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googleaccountnameviewmodel
		:rtype  GoogleCloudAccountGet

		"""
		route = f'{GoogleCloudAccountConsts.GOOGLE_CLOUD_ACCOUNT.value}/{gcp_cloud_account_id}/{GoogleCloudAccountConsts.ACCOUNT_NAME_ROUTE}'
		return self._put(route=route, body=body)

	def delete(self, google_cloud_account_id: str) -> None:
		"""Delete a Google cloud account (from Dome9)

		:link: https://api-v2-docs.dome9.com/index.html#googlecloudaccount_delete
		:param google_cloud_account_id: The Id of the Google cloud account
		:type  google_cloud_account_id: str
		:return: None

		"""
		route = f'{GoogleCloudAccountConsts.GOOGLE_CLOUD_ACCOUNT.value}/{google_cloud_account_id}'
		return self._delete(route=route)

	def update_account_gsuite(self, google_cloud_account_id: str, body: GoogleAccountGsuite) -> Dict:
		"""Update a Google Cloud account Gsuite data
		
		:link https://api-v2-docs.dome9.com/index.html#googlecloudaccount_updateaccountgsuite
		:param  google_cloud_account_id: The Id of the Google cloud account
		:type   google_cloud_account_id: str
		:param  body: the updated Gsuite as it will uses in Dome9
		:type   body: GoogleAccountGsuite
		:return https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googlecloudaccountgetviewmodel
		:rtype  GoogleCloudAccountGet

		"""
		route = f'{GoogleCloudAccountConsts.GOOGLE_CLOUD_ACCOUNT.value}/{google_cloud_account_id}/{GoogleCloudAccountConsts.CREDENTIALS.value}/{GoogleCloudAccountConsts.GSUITE.value}'
		return self._put(route=route, body=body)

	def update_google_cloud_account_credentials(self, google_cloud_account_id: str, body: GoogleCloudAccountUpdate, skip_compute_validation: bool = False) -> Dict:
		"""Update Google Cloud Account Credentials

		:link https://api-v2-docs.dome9.com/index.html#googlecloudaccount_updategooglecloudaccountcredentials
		:param  google_cloud_account_id: The Id of the Google cloud account
		:type   google_cloud_account_id: str
		:param  body: google cloudAccount update object
		:type   body: GoogleCloudAccountUpdate
		:param  skip_compute_validation: if true will skip compute validation
		:type   skip_compute_validation: bool
		:return https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googlecloudaccountupdateviewmodel
		:rtype  GoogleCloudAccountGet

		"""
		route = f'{GoogleCloudAccountConsts.GOOGLE_CLOUD_ACCOUNT.value}/{google_cloud_account_id}/{GoogleCloudAccountConsts.CREDENTIALS.value}'
		return self._put(route=route, params={'skipComputeValidation': skip_compute_validation}, body=body)

	def move_cloud_accounts_to_organizational_unit(self, body: MoveOrganizationalUnit) -> Dict:
		"""Detach cloud accounts from an Organizational unit and attach them to another Organizational unit Use 'null' for root organizational unit

		:link    https://api-v2-docs.dome9.com/index.html#googlecloudaccount_movecloudaccountstoorganizationalunit
		:param   body: move organizational unit object
		:type    body: MoveOrganizationalUnit
		:return: None
		
		"""
		route = f'{GoogleCloudAccountConsts.GOOGLE_CLOUD_ACCOUNT.value}/{GoogleCloudAccountConsts.ORGANIZATIONAL_UNIT_MOVE.value}'
		return self._put(route=route, body=body)

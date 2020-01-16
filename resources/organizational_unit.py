from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

from dome9 import Dome9Resource, Client, BaseDataclassRequest


class OrganizationalUnitConsts(Enum):

	ORGANIZATIONAL_UNIT_ROUTE      = 'OrganizationalUnit'
	FLAT_ORGANIZATIONAL_UNIT_ROUTE = 'GetFlatOrganizationalUnits'
	CLOUD_ACCOUNTS_ROUTE           = 'cloudaccounts'
	DELETE_ALL_ROUTE               = 'deleteAll'
	ORGANIZATIONAL_UNIT_ID         = 'id'


@dataclass
class OrganizationalUnitRequest(BaseDataclassRequest):
	"""Organizational unit update request

	Args:
		name (str): (Required) Name of the organizational unit
		parent_id (str): (Optional) Path should be in the format of 'parent-id'.'parent-id'

	"""
	name: str
	parent_id: str = None


class OrganizationalUnit(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: OrganizationalUnitRequest) -> Dict:
		"""Create a new OU

		:link https://api-v2-docs.dome9.com/#organizationalunit_postorganizationalunitasync
		:param body: The organizational unit data, requires name
		:type body: OrganizationalUnitRequest
		:return: Dict[Dict] with created ou item

		"""
		return self._post(route=OrganizationalUnitConsts.ORGANIZATIONAL_UNIT_ROUTE.value, body=body)

	def get(self, organizational_unit_id: str) -> Dict:
		"""Get OU by id

		:link https://api-v2-docs.dome9.com/#organizationalunit_get
		:param organizational_unit_id: Requested organizational unit id
		:type organizational_unit_id: str[uuid]
		:return: Dict with ou item

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT_ROUTE.value}/{organizational_unit_id}'

		return self._get(route=route)


	def get_all_cloud_accounts(self) -> Dict:
		"""Get all cloud accounts metadata (parent, child OUs and Cloud Accounts)

		:link https://api-v2-docs.dome9.com/#organizationalunit_getorganizationalunitcloudaccountsasync
		:return: Dict with cloud accounts metadata
		"""

		return self.get_organizational_unit_cloud_accounts(organizational_unit_id='')


	def get_organizational_unit_cloud_accounts(self, organizational_unit_id: str) -> Dict:
		"""Get cloud accounts attached to OU including child OUs and their cloud accounts

		:link https://api-v2-docs.dome9.com/#organizationalunit_getorganizationalunitcloudaccountsasync
		:param organizational_unit_id: Requested organizational unit id if empty will return all OUs and their Cloud Accounts
		:type organizational_unit_id: str[uuid]
		:return: Dict with organizational unit cloud accounts metadata

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT_ROUTE.value}/{OrganizationalUnitConsts.CLOUD_ACCOUNTS_ROUTE.value}'

		return self._get(route=route, params={OrganizationalUnitConsts.ORGANIZATIONAL_UNIT_ID.value: organizational_unit_id })

	def get_all_organizational_units(self) -> List[Dict]:
		"""Get all OUs flat

		:link https://api-v2-docs.dome9.com/#organizationalunit_getflatorganizationalunitsasync
		:return: List[Dict] with all OUs

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT_ROUTE.value}/{OrganizationalUnitConsts.FLAT_ORGANIZATIONAL_UNIT_ROUTE.value}'

		return self._get(route=route)

	def update(self, organizational_unit_id: str, body: OrganizationalUnitRequest) -> Dict:
		"""Update OU by id

		:link https://api-v2-docs.dome9.com/#organizationalunit_updatebyidasync
		:param organizational_unit_id:
		:type organizational_unit_id: str[uuid]
		:param body: The organizational unit data, requires name
		:type body: OrganizationalUnitRequest
		:return: Dict with ou item properties, its parent and children

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT_ROUTE.value}/{organizational_unit_id}'

		return self._put(route=route, body=body)

	def delete(self, organizational_unit_id: str) -> None:
		"""Delete OU by id and attach its cloud accounts to the the root OU

		:link https://api-v2-docs.dome9.com/#organizationalunit_deleteorganizationalunitbyidasync
		:param organizational_unit_id: OU id to delete
		:type organizational_unit_id: str[uuid]
		:return: None

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT_ROUTE.value}/{organizational_unit_id}'

		return self._delete(route=route)

	def delete_all_organizational_units(self) -> None:
		"""Delete all OUs, detach all cloud accounts from the OUs they belong to
		and attach them to the root OU

		:link https://api-v2-docs.dome9.com/#organizationalunit_deleteallorganizationalunitsasync
		:return: None

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT_ROUTE.value}/{OrganizationalUnitConsts.DELETE_ALL_ROUTE.value}'

		return self._delete(route=route)
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

from dome9 import Dome9Resource, Client, BaseDataclassRequest


class OrganizationalUnitConsts(Enum):

	ORGANIZATIONAL_UNIT = 'OrganizationalUnit'
	FLAT_ORGANIZATIONAL_UNIT = 'GetFlatOrganizationalUnits'
	CLOUD_ACCOUNTS = 'cloudaccounts'
	DELETE_ALL = 'deleteAll'
	ORGANIZATIONAL_UNIT_ID = 'id'


@dataclass
class OrganizationalUnitRequest(BaseDataclassRequest):
	"""Organizational unit update request

	:link  https://api-v2-docs.dome9.com/#schemafalconetix-model-organizationalunit-organizationalunitviewmodel
	:param name: (Required) Name of the organizational unit
	:type  name: str
	:param parent_id: (Optional) Path should be in the format of 'parent-id'.'parent-id'
	:type  parent_id: str

	"""
	name: str
	parent_id: str = None


class OrganizationalUnit(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: OrganizationalUnitRequest) -> Dict:
		"""Create a new OU

		:link   https://api-v2-docs.dome9.com/#organizationalunit_postorganizationalunitasync
		:param  body: The organizational unit data, requires name
		:type   body: OrganizationalUnitRequest
		:return https://api-v2-docs.dome9.com/#schemadome9-bl-std-helpers-treenode_falconetix-model-organizationalunit-organizationalunitentitytreeitem_system-string_
		:rtype  String_

		"""
		return self._post(route=OrganizationalUnitConsts.ORGANIZATIONAL_UNIT.value, body=body)

	def get(self, organizational_unit_id: str) -> Dict:
		"""Get OU by id

		:link   https://api-v2-docs.dome9.com/#organizationalunit_get
		:param  organizational_unit_id: Requested organizational unit id
		:type   organizational_unit_id: str[uuid]
		:return https://api-v2-docs.dome9.com/#schemadome9-bl-std-helpers-treenode_falconetix-model-organizationalunit-organizationalunitentitytreeitem_system-string_
		:rtype  String_

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT.value}/{organizational_unit_id}'

		return self._get(route=route)

	def get_all_cloud_accounts(self) -> Dict:
		"""Get all cloud accounts metadata (parent, child OUs and Cloud Accounts)

		:link   https://api-v2-docs.dome9.com/#organizationalunit_getorganizationalunitcloudaccountsasync
		:return Dict with cloud accounts metadata
		:rtype  Dict

		"""

		return self.get_organizational_unit_cloud_accounts(organizational_unit_id='')

	def get_organizational_unit_cloud_accounts(self, organizational_unit_id: str) -> Dict:
		"""Get cloud accounts attached to OU including child OUs and their cloud accounts

		:link   https://api-v2-docs.dome9.com/#organizationalunit_getorganizationalunitcloudaccountsasync
		:param  organizational_unit_id: Requested organizational unit id if empty will return all OUs and their Cloud Accounts
		:type   organizational_unit_id: str[uuid]
		:return Dict with organizational unit cloud accounts metadata
		:rtype  Dict

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT.value}/{OrganizationalUnitConsts.CLOUD_ACCOUNTS.value}'

		return self._get(route=route, params={OrganizationalUnitConsts.ORGANIZATIONAL_UNIT_ID.value: organizational_unit_id})

	def get_all_organizational_units(self) -> List[Dict]:
		"""Get all OUs flat

		:link   https://api-v2-docs.dome9.com/#organizationalunit_getflatorganizationalunitsasync
		:return https://api-v2-docs.dome9.com/#schemafalconetix-model-organizationalunit-organizationalunitviewmodel
		:rtype  OrganizationalUnit

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT.value}/{OrganizationalUnitConsts.FLAT_ORGANIZATIONAL_UNIT.value}'

		return self._get(route=route)

	def update(self, organizational_unit_id: str, body: OrganizationalUnitRequest) -> Dict:
		"""Update OU by id

		:link   https://api-v2-docs.dome9.com/#organizationalunit_updatebyidasync
		:param  organizational_unit_id:
		:type   organizational_unit_id: str[uuid]
		:param  body: The organizational unit data, requires name
		:type   body: OrganizationalUnitRequest
		:return https://api-v2-docs.dome9.com/#schemadome9-bl-std-helpers-treenode_falconetix-model-organizationalunit-organizationalunitentitytreeitem_system-string_
		:rtype  String_

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT.value}/{organizational_unit_id}'

		return self._put(route=route, body=body)

	def delete(self, organizational_unit_id: str) -> Dict:
		"""Delete OU by id and attach its cloud accounts to the the root OU

		:link   https://api-v2-docs.dome9.com/#organizationalunit_deleteorganizationalunitbyidasync
		:param  organizational_unit_id: OU id to delete
		:type   organizational_unit_id: str[uuid]
		:return https://api-v2-docs.dome9.com/#schemadome9-bl-std-helpers-treenode_falconetix-model-organizationalunit-organizationalunitentitytreeitem_system-string_
		:rtype  String_

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT.value}/{organizational_unit_id}'

		return self._delete(route=route)

	def delete_all_organizational_units(self) -> None:
		"""Delete all OUs, detach all cloud accounts from the OUs they belong to
		   and attach them to the root OU

		:link   https://api-v2-docs.dome9.com/#organizationalunit_deleteallorganizationalunitsasync
		:return None

		"""
		route = f'{OrganizationalUnitConsts.ORGANIZATIONAL_UNIT.value}/{OrganizationalUnitConsts.DELETE_ALL.value}'

		return self._delete(route=route)

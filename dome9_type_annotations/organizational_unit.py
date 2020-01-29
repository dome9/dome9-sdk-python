from typing import Dict, List

from resources.organizational_unit import OrganizationalUnit as BaseOrganizationalUnit, OrganizationalUnitRequest


class organizational_unit(BaseOrganizationalUnit):

	@classmethod
	def create(cls, body: OrganizationalUnitRequest) -> Dict:
		"""Create a new OU

		:link   https://api-v2-docs.dome9.com/#organizationalunit_postorganizationalunitasync
		:param  body: The organizational unit data, requires name
		:type   body: OrganizationalUnitRequest
		:return https://api-v2-docs.dome9.com/#schemadome9-bl-std-helpers-treenode_falconetix-model-organizationalunit-organizationalunitentitytreeitem_system-string_
		:rtype  String_

		"""
		pass

	@classmethod
	def get(cls, organizational_unit_id: str) -> Dict:
		"""Get OU by id

		:link   https://api-v2-docs.dome9.com/#organizationalunit_get
		:param  organizational_unit_id: Requested organizational unit id
		:type   organizational_unit_id: str[uuid]
		:return https://api-v2-docs.dome9.com/#schemadome9-bl-std-helpers-treenode_falconetix-model-organizationalunit-organizationalunitentitytreeitem_system-string_
		:rtype  String_

		"""
		pass

	@classmethod
	def get_organizational_unit_cloud_accounts(cls, organizational_unit_id: str = '') -> Dict:
		"""Get cloud accounts attached to OU including child OUs and their cloud accounts

		:link   https://api-v2-docs.dome9.com/#organizationalunit_getorganizationalunitcloudaccountsasync
		:param  organizational_unit_id: (Optional) Requested organizational unit id if empty will return all OUs and their Cloud Accounts
		:type   organizational_unit_id: str[uuid]
		:return Dict with organizational unit cloud accounts metadata
		:rtype  Dict

		"""
		pass

	@classmethod
	def get_all_organizational_units(cls) -> List[Dict]:
		"""Get all OUs flat

		:link   https://api-v2-docs.dome9.com/#organizationalunit_getflatorganizationalunitsasync
		:return https://api-v2-docs.dome9.com/#schemafalconetix-model-organizationalunit-organizationalunitviewmodel
		:rtype  OrganizationalUnit

		"""
		pass

	@classmethod
	def update(cls, organizational_unit_id: str, body: OrganizationalUnitRequest) -> Dict:
		"""Update OU by id

		:link   https://api-v2-docs.dome9.com/#organizationalunit_updatebyidasync
		:param  organizational_unit_id:
		:type   organizational_unit_id: str[uuid]
		:param  body: The organizational unit data, requires name
		:type   body: OrganizationalUnitRequest
		:return https://api-v2-docs.dome9.com/#schemadome9-bl-std-helpers-treenode_falconetix-model-organizationalunit-organizationalunitentitytreeitem_system-string_
		:rtype  String_

		"""
		pass

	@classmethod
	def delete(cls, organizational_unit_id: str) -> Dict:
		"""Delete OU by id and attach its cloud accounts to the the root OU

		:link   https://api-v2-docs.dome9.com/#organizationalunit_deleteorganizationalunitbyidasync
		:param  organizational_unit_id: OU id to delete
		:type   organizational_unit_id: str[uuid]
		:return https://api-v2-docs.dome9.com/#schemadome9-bl-std-helpers-treenode_falconetix-model-organizationalunit-organizationalunitentitytreeitem_system-string_
		:rtype  String_

		"""
		pass

	@classmethod
	def delete_all_organizational_units(cls) -> None:
		"""Delete all OUs, detach all cloud accounts from the OUs they belong to
		   and attach them to the root OU

		:link   https://api-v2-docs.dome9.com/#organizationalunit_deleteallorganizationalunitsasync
		:return None

		"""
		pass

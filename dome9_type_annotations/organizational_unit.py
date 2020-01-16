from typing import Dict, List

from resources.organizational_unit import OrganizationalUnit as BaseOrganizationalUnit, OrganizationalUnitRequest


class organizational_unit(BaseOrganizationalUnit):

	@classmethod
	def create(cls, body: OrganizationalUnitRequest) -> Dict:
		pass

	@classmethod
	def get(cls, organizational_unit_id: str) -> Dict:
		pass

	@classmethod
	def get_all_organizational_units(cls) -> List[Dict]:
		pass

	@classmethod
	def get_organizational_unit_cloud_accounts(cls, organizational_unit_id: str) -> Dict:
		pass

	@classmethod
	def get_all_cloud_accounts(cls) -> Dict:
		pass

	@classmethod
	def update(cls, organizational_unit_id: str, body: OrganizationalUnitRequest) -> Dict:
		pass

	@classmethod
	def delete(cls, organizational_unit_id: str) -> None:
		pass

	@classmethod
	def delete_all_organizational_units(cls) -> None:
		pass
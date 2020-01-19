from typing import Dict, List, Union

from resources.role import Role as BaseRole, RoleRequest


class role(BaseRole):

	@classmethod
	def create(cls, body: RoleRequest) -> Dict:
		pass

	@classmethod
	def get(cls, role_id: str = '') -> Union[Dict, List[Dict]]:
		pass

	@classmethod
	def update(cls, role_id: str, body: RoleRequest) -> Dict:
		pass

	@classmethod
	def delete(cls, role_id: str) -> None:
		pass

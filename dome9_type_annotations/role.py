from typing import Dict, List, Union

from resources.role import Role as BaseRole, CreateRole, UpdateRole


class role(BaseRole):

	@classmethod
	def create(cls, body: CreateRole) -> Dict:
		"""Create a new role

		:link   https://api-v2-docs.dome9.com/#role_post
		:param  body: The role info
		:type   body: RoleRequest
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-role-roleviewmodel
		:rtype  Role

		"""
		pass

	@classmethod
	def get(cls, role_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get the specific role with the specified id

		:param  role_id: The role id
		:type   role_id: str
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-role-roleviewmodel
		:rtype  Role

		"""
		pass

	@classmethod
	def update(cls, role_id: str, body: UpdateRole) -> Dict:
		"""Update a role

		:param  role_id: The role id
		:type   role_id: str
		:param  body: The role info
		:type   body: RoleRequest
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-role-roleviewmodel
		:rtype  Role

		"""
		pass

	@classmethod
	def delete(cls, role_id: str) -> None:
		"""

		:param   role_id: The role id to delete
		:type    role_id: str
		:return: None

		"""
		pass

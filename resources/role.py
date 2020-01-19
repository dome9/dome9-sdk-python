from dataclasses import dataclass
from enum import Enum
from typing import Union, Dict, List

from dome9 import Dome9Resource, Client, BaseDataclassRequest


class RoleConsts(Enum):
	MAIN_ROUTE = 'role'


@dataclass
class Permissions(BaseDataclassRequest):
	"""Permissions

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-user-permissionsviewmodel
	:param access: Access permission list (list of SRL)
	:type  access: list(str)
	:param manage: Manage permission list (list of SRL)
	:type  manage: list(str)
	:param rulesets: Compliance permission list (list of SRL)
	:type  rulesets: list(str)
	:param notifications: Compliance permission list (list of SRL)
	:type  notifications: list(str)
	:param policies: Compliance permission list (list of SRL)
	:type  policies: list(str)
	:param alert_actions: Compliance permission list (list of SRL)
	:type  alert_actions: list(str)
	:param create: Create permission list (list of SRL)
	:type  create: list(str)
	:param view: View permission list (list of SRL)
	:type  view: list(str)
	:param on_boarding: View permission SRL
	:type  on_boarding: list(str)

	"""
	access: List[str] = ()
	manage: List[str] = ()
	rulesets: List[str] = ()
	notifications: List[str] = ()
	policies: List[str] = ()
	alert_actions: List[str] = ()
	create: List[str] = ()
	view: List[str] = ()
	on_boarding: List[str] = ()


@dataclass
class CreateRole(BaseDataclassRequest):
	"""Role

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-role-roleviewmodel
	:param name: Role Name
	:type  name: str
	:param description: description
	:type  description: str
	:param permissions: Permissions of the role
	:type  permissions: Permissions

	"""
	name: str
	description: str


@dataclass
class UpdateRole(BaseDataclassRequest):
	"""Role

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-role-roleviewmodel
	:param name: Role Name
	:type  name: str
	:param description: description
	:type  description: str
	:param permissions: Permissions of the role
	:type  permissions: Permissions

	"""
	name: str
	description: str
	permissions: Permissions


class Role(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: CreateRole) -> Dict:
		"""Create a new role

		:link   https://api-v2-docs.dome9.com/#role_post
		:param  body: The role info
		:type   body: RoleRequest
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-role-roleviewmodel
		:rtype  Role

		"""
		return self._post(route=RoleConsts.MAIN_ROUTE.value, body=body)

	def get(self, role_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get the specific role with the specified id

		:param  role_id: The role id
		:type   role_id: str
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-role-roleviewmodel
		:rtype  Role

		"""
		route = f'{RoleConsts.MAIN_ROUTE.value}/{role_id}'
		return self._get(route=route)

	def update(self, role_id: str, body: UpdateRole) -> Dict:
		"""Update a role

		:param  role_id: The role id
		:type   role_id: str
		:param  body: The role info
		:type   body: RoleRequest
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-role-roleviewmodel
		:rtype  Role

		"""
		route = f'{RoleConsts.MAIN_ROUTE.value}/{role_id}'
		return self._put(route=route, body=body)

	def delete(self, role_id: str) -> None:
		"""

		:param  role_id: The role id to delete
		:type   role_id: str
		:return: None

		"""
		route = f'{RoleConsts.MAIN_ROUTE.value}/{role_id}'
		return self._delete(route=route)

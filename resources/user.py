from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union

from dome9 import BaseDataclassRequest, Dome9Resource, Client


class UserConsts(Enum):
	USER = 'user'
	ACCOUNT_OWNER = 'account/owner'


@dataclass
class Permissions:
	"""Update users role_ids and permissions
		:param    access
		:type     access: List[str]
		:param    manage
		:type     manage: List[str]
		:param    rule_sets
		:type     rule_sets: List[str]
		:param    notifications
		:type     notifications: List[str]
		:param    alert_actions
		:type     alert_actions: List[str]
		:param    create
		:type     create: List[str]
		:param    view
		:type     view: List[str]
		:param    on_boarding
		:type     on_boarding: List[str]
		:param    cross_account_access
		:type     cross_account_access: List[str]


	"""
	access: List[str]
	manage: List[str]
	rule_sets: List[str]
	notifications: List[str]
	policies: List[str]
	alert_actions: List[str]
	create: List[str]
	view: List[str]
	on_boarding: List[str]
	cross_account_access: List[str]


@dataclass
class UserRequest(BaseDataclassRequest):
	"""User request
	
	:param    email
	:type     email: str
	:param    first_name
	:type     first_name: str
	:param    last_name
	:type     last_name: str
	:param    sso_enabled: User has enabled SSO sign-on
	:type     sso_enabled: bool

	"""
	email: str
	first_name: str
	last_name: str
	sso_enabled: bool


@dataclass
class UpdateUser(BaseDataclassRequest):
	"""Update users role_ids and permissions

	:param    email
	:type     email: str
	:param    first_name
	:type     first_name: str
	:param    last_name
	:type     last_name: str
	:param    sso_enabled: User has enabled SSO sign-on
	:type     sso_enabled: bool

	"""
	permissions: Permissions
	role_ids: List[int] = None


@dataclass
class SetAsOwner(BaseDataclassRequest):
	"""Set user as owner data

	:param    user_id
	:type     user_id: str

	"""
	user_id: str


class User(Dome9Resource):
	user_email_id = {}

	def __init__(self, client: Client):
		super().__init__(client)

	@staticmethod
	def _remove_key_by_value(value_to_delete) -> None:
		for key, val in User.user_email_id.items():
			if value_to_delete == val:
				del User.user_email_id[key]

	# update global dict where the key is users email and the value is users id
	def _refresh_user_email_id_map(self) -> None:
		users = self.get()
		for user in users:
			User.user_email_id[user['name']] = user['id']

	def create(self, body: UserRequest) -> Dict:
		"""Create user in dome9

		:param body: Details for the new user
		:type body: UserRequest
		:returns: Dict that has metadata for the created user in dome9

		"""
		resp = self._post(route=UserConsts.USER.value, body=body)
		User.user_email_id[resp['name']] = resp['id']
		return resp

	def get(self, user_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get all Dome9 users for the Dome9 account.

		:link   https://api-v2-docs.dome9.com/index.html#user_get
		:param  user_id: Dome9 user id
		:type   user_id: str
		:return https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-user-userviewmodel
		:rtype  Dict

		"""
		route = f'{UserConsts.USER.value}/{user_id}'
		return self._get(route=route)

	def update(self, user_id: str, body: UpdateUser) -> Dict:
		"""Update the user with the specified id

		:link   https://api-v2-docs.dome9.com/index.html#user_put
		:param  user_id: Dome9 user id
		:type   user_id: str
		:param  body: Details for the user
		:type   body: UpdateUser
		:return 200 OK
		:rtype  Dict

		"""
		route = f'{UserConsts.USER.value}/{user_id}'
		return self._put(route=route, body=body)

	def set_as_owner(self, body: SetAsOwner) -> None:
		"""Update users Roles or permissions

		:link
		:param body: Set user as owner details
		:type body: SetAsOwner
		:return: metadata for user object
		:rtype: Dict

		"""
		return self._put(route=UserConsts.ACCOUNT_OWNER.value, body=body)

	def delete(self, user_id: str) -> None:
		"""Delete a user

		:link    https://api-v2-docs.dome9.com/index.html#user_delete
		:param   user_id: Dome9 user id
		:type    user_id: str
		:return: None

		"""
		route = f'{UserConsts.USER.value}/{user_id}'
		response = self._delete(route=route)
		User._remove_key_by_value(value_to_delete=user_id)
		return response

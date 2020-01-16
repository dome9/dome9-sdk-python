from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from dome9 import BaseDataclassRequest, Dome9Resource, Client


class UserConsts(Enum):
	MAIN_ROUTE = 'user'
	OWNER_ROUTE = 'account/owner'


@dataclass
class Permissions:
	"""Update users role_ids and permissions

		Args:
			access (List[str]): access
			manage (List[str]): manage
			rulesets (List[str]): rulesets
			notifications (List[str]): notifications
			policies (List[str]): policies
			alert_actions (List[str]): alert actions
			create (List[str]): create
			view (List[str]): view
			on_boarding (List[str]): on boarding
			cross_account_access (List[str]): cross account access
	"""
	access: List[str]
	manage: List[str]
	rulesets: List[str]
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

		Args:
			email (str): User email
			first_name (str): First name
			last_name (str): Last name
			sso_enabled (bool): User has enabled SSO sign-on

	"""
	email: str
	first_name: str
	last_name: str
	sso_enabled: bool


@dataclass
class UpdateUser(BaseDataclassRequest):
	"""Update users role_ids and permissions

		Args:
			email (str): User email
			first_name (str): First name
			last_name (str): Last name
			sso_enabled (bool): User has enabled SSO sign-on

	"""
	permissions: Permissions
	role_ids: List[int] = None


@dataclass
class SetAsOwner(BaseDataclassRequest):
	"""Set user as owner data

		Args:
			user_id (str): User id

	"""
	user_id: str


class User(Dome9Resource):
	user_email_id = {}

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: UserRequest) -> Dict:
		"""Create user in dome9

		:param body: Details for the new user
		:type body: UserRequest
		:returns: Dict that has metadata for the created user in dome9

		"""
		resp = self._post(route=UserConsts.MAIN_ROUTE.value, body=body)
		User.user_email_id[resp['name']] = resp['id']
		return resp

	def get(self, user_id: str) -> Dict:
		"""Get user

		:param user_id: Dome9 user id
		:type user_id: str
		:returns: Dict that has metadata for user

		"""
		route = f'{UserConsts.MAIN_ROUTE.value}/{user_id}'
		return self._get(route=route)

	def get_all(self) -> List[Dict]:
		"""Get all users in dome9

		:returns: List of dicts that has metadata for all users

		"""
		return self._get(route=UserConsts.MAIN_ROUTE.value)

	def update(self, user_id: str, body: UpdateUser) -> Dict:
		"""Update users Roles or permissions

		:param user_id: Dome9 user id
		:type user_id: str
		:param body: Details for the user
		:type body: UpdateUser

		:returns: Dict that has metadata for the updated user

		"""
		route = f'{UserConsts.MAIN_ROUTE.value}/{user_id}'
		return self._put(route=route, body=body)

	def set_as_owner(self, body: SetAsOwner) -> None:
		"""Update users Roles or permissions

		:param body: Set user as owner details
		:type body: SetAsOwner

		:returns: Dict that has metadata for user

		"""
		return self._put(route=UserConsts.OWNER_ROUTE.value, body=body)

	def delete(self, user_id: str) -> None:
		"""Delete dome9 user

		:param user_id: Dome9 user id
		:type user_id: str
		:returns: None

		"""
		route = f'{UserConsts.MAIN_ROUTE.value}/{user_id}'
		return self._delete(route=route)

	# update global dict where the key is users email and the value is users id
	def _refresh_user_email_id_map(self) -> None:
		users = self.get_all()
		for user in users:
			User.user_email_id[user['name']] = user['id']

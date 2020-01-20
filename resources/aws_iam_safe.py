from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from loguru import logger

from dome9 import Client, BaseDataclassRequest, Dome9Resource, APIUtils
from dome9.consts import EntityType
from resources.aws_cloud_account import AwsCloudAccountConsts
from resources.user import UserConsts, User


class AwsIamSafeConsts(Enum):
	IAM_SAFE_ROUTE = 'iam-safe'
	IAM_ENTITY_ROUTE = 'iamEntities'
	RESTRICTED_IAM_ROUTE = 'restrictedIamEntities'
	IAM_ENTITIES_ROUTE = 'iam'
	ENTITY_NAME = 'entityName'
	ACCOUNTS = "accounts"
	ROLES_ARN = "rolesArns"
	USERS_ARN = "usersArns"


@dataclass
class IAMSafeData:
	"""IAM safe data

		Args:
			aws_group_arn(str): (Required) AWS group arn.
			aws_policy_arn(str): (Required) AWS policy arn.

	"""
	aws_group_arn: str
	aws_policy_arn: str


@dataclass
class AttachIamSafe(BaseDataclassRequest):
	"""IAMSafeData

		Args:
			cloud_account_id(str): (Required) AWS cloud account to attach IAM safe to it.
			data(str): (Required) IAM safe data

	"""
	cloud_account_id: str
	data: IAMSafeData


@dataclass
class RestrictedIamEntitiesRequest(BaseDataclassRequest):
	"""Restricted iam entities request

		Args:
			entity_type (str): Entity type, must be one of the following Role or User
			entity_name (str): Aws iam user name or aws role

	"""
	entity_type: str
	entity_name: str

	@logger.catch(reraise=True)
	def __post_init__(self):
		APIUtils.check_is_valid_entity_type(entity_type=self.entity_type)


@dataclass
class ProtectIamSafeWithElevation(BaseDataclassRequest):
	"""Protect iam safe with elevation

		Args:
			iam_entities (List[str]): Iam entities

	"""
	iam_entities: List[str]


class AwsIamSafe(Dome9Resource):

	def __init__(self, client: Client):
		User(client=client)._refresh_user_email_id_map()
		super().__init__(client)

	# attach iam safe to cloud account
	def attach_iam_safe(self, body: AttachIamSafe) -> Dict:
		"""Attach iam safe to aws cloud account

		:param body: Details for aws cloud account in order to attach to iam safe
		:type body: AttachIamSafe
		:returns: Dict that has metadata for attached aws cloud account

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsIamSafeConsts.IAM_SAFE_ROUTE.value}'
		return self._put(route=route, body=body)

	def detach_iam_safe(self, aws_cloud_account_id: str) -> None:
		"""Detach iam safe to aws cloud account

		:param aws_cloud_account_id: Aws cloud account id
		:type aws_cloud_account_id: str
		:returns: Dict that has metadata for attached aws cloud account

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsIamSafeConsts.IAM_SAFE_ROUTE.value}'
		return self._delete(route=route)

	# iam protect (restrict) entity
	def protect_iam_safe(self, aws_cloud_account_id: str, body: RestrictedIamEntitiesRequest) -> str:
		"""Protect iam safe entity where the entity can be User or Role

		:param aws_cloud_account_id: Aws security group id.
		:type aws_cloud_account_id: str
		:param body: Details restricted iam entities request
		:type body: RestrictedIamEntitiesRequest
		:returns: Aws User or Role arn that protected

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsIamSafeConsts.RESTRICTED_IAM_ROUTE.value}'
		return self._post(route=route, body=body)

	def get_all_protected_iam_safe(self, aws_cloud_account_id: str) -> Dict:
		"""Get data for all the users and roles

		:param aws_cloud_account_id: Aws security group id.
		:type aws_cloud_account_id: str
		:returns: Dict that has two key, roles and users

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsIamSafeConsts.IAM_ENTITIES_ROUTE.value}'
		return self._get(route=route)

	def unprotect_iam_safe(self, aws_cloud_account_id: str, entity_type: str, entity_name: str) -> None:
		"""Unprotect specific iam safe entity

		:param aws_cloud_account_id: Aws security group id.
		:type aws_cloud_account_id: str
		:param entity_type: entity type, must be User or Role
		:type entity_type: str
		:param entity_name: Entity name
		:type entity_name: str
		:returns: None

		"""
		APIUtils.check_is_valid_entity_type(entity_type=entity_type)

		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsIamSafeConsts.RESTRICTED_IAM_ROUTE.value}/{entity_type}'
		return self._delete(route=route, params={AwsIamSafeConsts.ENTITY_NAME.value: entity_name})

	# iam protect with elevation
	def protect_iam_safe_with_elevation(self, aws_cloud_account_id: str, entity_name: str, entity_type: str, users_ids_to_protect: List[str]) -> None:
		"""Protect iam safe with elevation

		:param aws_cloud_account_id: Aws security group id.
		:type aws_cloud_account_id: str
		:param entity_name: Aws iam user name or aws role
		:type entity_name: str
		:param entity_type: Entity type, must be one of the following Role or User
		:type entity_type: str
		:param users_ids_to_protect: List of users ids to protect
		:type users_ids_to_protect: List[str]
		:return: None

		"""
		APIUtils.check_is_valid_entity_type(entity_type=entity_type)

		entities_failed_to_protect = set()
		entity_details = self._get_iam_entity_details(aws_cloud_account_id=aws_cloud_account_id,
			entity_name=entity_name,
			entity_type=entity_type)
		body = ProtectIamSafeWithElevation(iam_entities=[entity_details['arn']])

		for user_id in users_ids_to_protect:
			route = f'{UserConsts.USER.value}/{user_id}/{AwsIamSafeConsts.IAM_SAFE_ROUTE.value}/{AwsIamSafeConsts.ACCOUNTS.value}/{aws_cloud_account_id}/{AwsIamSafeConsts.IAM_ENTITY_ROUTE.value}'
			resp = self._post(route=route, body=body)
			if len(resp['failedIamEntities']) != 0:
				entities_failed_to_protect.add(user_id)

		if len(entities_failed_to_protect) != 0:
			logger.warning(f'failed to protect the following users with ids {entities_failed_to_protect}')

	def update_iam_safe_with_elevation(self, aws_cloud_account_id: str, entity_name: str, entity_type: str,  users_ids_to_protect: List[str]) -> None:
		"""Protect iam safe with elevation

		:param aws_cloud_account_id: Aws security group id.
		:type aws_cloud_account_id: str
		:param entity_name: Aws iam user name or aws role
		:type entity_name: str
		:param entity_type: Entity type, must be one of the following Role or User
		:type entity_type: str
		:param users_ids_to_protect: List of users ids to protect
		:type users_ids_to_protect: List[str]
		:return: None

		"""

		APIUtils.check_is_valid_entity_type(entity_type=entity_type)
		entities_failed_to_protect = set()

		entity_details = self._get_iam_entity_details(aws_cloud_account_id=aws_cloud_account_id, entity_name=entity_name, entity_type=entity_type)
		curr_protected_users_ids = AwsIamSafe._get_users_ids_according_to_emails(emails=entity_details['attachedDome9Users'])
		protected_unprotected_dict = AwsIamSafe._generate_protected_unprotected_map(curr_protected_users_ids=curr_protected_users_ids, users_ids_to_protect=users_ids_to_protect)

		unprotect_body = ProtectIamSafeWithElevation(iam_entities=[])
		protect_body = ProtectIamSafeWithElevation(iam_entities=[entity_details['arn']])

		for user_id, to_protect in protected_unprotected_dict.items():
			route = f'{UserConsts.USER.value}/{user_id}/{AwsIamSafeConsts.IAM_SAFE_ROUTE.value}/{AwsIamSafeConsts.ACCOUNTS.value}/{aws_cloud_account_id}/{AwsIamSafeConsts.IAM_ENTITY_ROUTE.value}'
			if to_protect:
				resp = self._put(route=route, body=protect_body)
			else:
				resp = self._put(route=route, body=unprotect_body)

			if len(resp['failedIamEntities']) != 0:
				entities_failed_to_protect.add(user_id)

		if len(entities_failed_to_protect) != 0:
			logger.warning(f'failed to protect the following users with ids {entities_failed_to_protect}')

	def unprotect_iam_safe_with_elevation(self, aws_cloud_account_id: str, entity_name: str, entity_type: str) -> None:
		"""Protect iam safe with elevation

		:param aws_cloud_account_id: Aws security group id.
		:type aws_cloud_account_id: str
		:param entity_name: Aws iam user name or aws role
		:type entity_name: str
		:param entity_type: Entity type, must be one of the following Role or User
		:type entity_type: str
		:return: None

		"""
		APIUtils.check_is_valid_entity_type(entity_type=entity_type)

		# in order to unprotect iam safe with elevation, first protect iam safe (restrict) then unprotect
		body = RestrictedIamEntitiesRequest(entity_type=entity_type, entity_name=entity_name)
		self.protect_iam_safe(aws_cloud_account_id=aws_cloud_account_id, body=body)
		self.unprotect_iam_safe(aws_cloud_account_id=aws_cloud_account_id, entity_type=entity_type, entity_name=entity_name)

	# get details for iam entity
	def _get_iam_entity_details(self, aws_cloud_account_id: str, entity_name: str, entity_type: str) -> Dict:
		iam_entities = self.get_all_protected_iam_safe(aws_cloud_account_id=aws_cloud_account_id)
		iam_entities = iam_entities[AwsIamSafeConsts.ROLES_ARN.value] if entity_type == EntityType.ROLE.value else iam_entities[
			AwsIamSafeConsts.USERS_ARN.value]
		for entity in iam_entities:
			if entity['name'] == entity_name:
				return entity

	# get list of ids according to received email
	@staticmethod
	def _get_users_ids_according_to_emails(emails: List[str]) -> List[str]:
		users_ids = []
		for email in emails:
			users_ids.append(User.user_email_id[email])

		return users_ids

	# get dic where key is users id and value is bool where true indicated to protect the user and false to unprotect it
	@staticmethod
	def _generate_protected_unprotected_map(curr_protected_users_ids: List[str], users_ids_to_protect: List[str]) -> Dict[str, bool]:
		protected_unprotected = {}

		for curr_protected_user_id in curr_protected_users_ids:
			protected_unprotected[str(curr_protected_user_id)] = False

		for user_id_to_protect in users_ids_to_protect:
			# if the user already protected then there is to need to protect him
			if user_id_to_protect in protected_unprotected:
				del protected_unprotected[user_id_to_protect]
			else:
				protected_unprotected[user_id_to_protect] = True

		return protected_unprotected

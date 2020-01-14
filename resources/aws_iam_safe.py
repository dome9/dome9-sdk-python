from dataclasses import dataclass
from enum import Enum
from typing import Dict

from loguru import logger

from dome9 import Client, BaseDataclassRequest, Dome9Resource
from dome9.exceptions import UnsupportedCloudAccountEntityType
from resources.aws_cloud_account import AwsCloudAccountConsts


class AwsIamSafeConsts(Enum):
	IAM_SAFE_ROUTE = 'iam-safe'
	RESTRICTED_IAM_ROUTE = 'restrictedIamEntities'
	IAM_ENTITIES_ROUTE = 'iam'
	ENTITY_NAME = 'entityName'


class EntityType(Enum):
	ROLE = 'Role'
	USER = 'User'


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
			entity_name (str): Aws iam user name or aws role
			entity_type (str): Entity type, must be one of the following Role or User

	"""
	entity_name: str
	entity_type: str

	@logger.catch(reraise=True)
	def __post_init__(self):
		entityTypes = [entityType.value for entityType in EntityType]
		if self.entity_type not in entityTypes:
			raise UnsupportedCloudAccountEntityType(f'entity type must be one of the following {entityTypes}')


class AwsIamSafe(Dome9Resource):

	def __init__(self, client: Client):
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
	def protect_iam_safe_entity(self, aws_cloud_account_id: str, body: RestrictedIamEntitiesRequest) -> str:
		"""Protect iam safe entity where the entity can be User or Role

		:param aws_cloud_account_id: Aws security group id.
		:type aws_cloud_account_id: str
		:param body: Details restricted iam entities request
		:type body: RestrictedIamEntitiesRequest
		:returns: Aws User or Role arn that protected

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsIamSafeConsts.RESTRICTED_IAM_ROUTE.value}'
		return self._post(route=route, body=body)

	def get_all_protected_iam_safe_entity(self, aws_cloud_account_id: str) -> Dict:
		"""Get data for all the users and roles

		:param aws_cloud_account_id: Aws security group id.
		:type aws_cloud_account_id: str
		:returns: Dict that has two key, roles and users

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsIamSafeConsts.IAM_ENTITIES_ROUTE.value}'
		return self._get(route=route)

	def unprotect_iam_safe_entity(self, aws_cloud_account_id: str, entity_type: str, entity_name: str) -> None:
		"""Unprotect specific iam safe entity

		:param aws_cloud_account_id: Aws security group id.
		:type aws_cloud_account_id: str
		:param entity_type: entity type, must be User or Role
		:type entity_type: str
		:param entity_name: Entity name
		:type entity_name: str
		:returns: None

		"""
		entity_types = [entity_type.value for entity_type in EntityType]
		if entity_type not in entity_types:
			raise UnsupportedCloudAccountEntityType(f'entity type must be one of the following {entity_types}')

		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsIamSafeConsts.RESTRICTED_IAM_ROUTE.value}/{entity_type}'
		return self._delete(route=route, params={AwsIamSafeConsts.ENTITY_NAME.value: entity_name})

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from loguru import logger

from dome9 import APIUtils
from dome9.client import Client
from dome9.consts import AwsRegions, NewGroupBehaviors
from dome9.base_dataclass import BaseDataclassRequest
from dome9.exceptions import UnsupportedCloudAccountEntityType, UnsupportedCloudAccountCredentialsBasedType, UnsupportedCloudAccountGroupBehaviors

from dome9.resource import Dome9Resource


class AwsCloudAccountConsts(Enum):
	MAIN_ROUTE = 'CloudAccounts'
	REGION_CONFIG_ROUTE = 'region-conf'
	ORGANIZATIONAL_UNIT_ROUTE = 'organizationalUnit'
	NAME_ROUTE = 'name'
	CREDENTIALS_ROUTE = 'credentials'
	IAM_SAFE_ROUTE = 'iam-safe'
	RESTRICTED_IAM_ROUTE = 'restrictedIamEntities'
	IAM_ENTITIES_ROUTE = 'iam'
	ENTITY_NAME = 'entityName'


class AwsCloudAccountCredentialsBasedType(Enum):
	USER_BASED_TYPE = 'UserBased'
	ROLE_BASED_TYPE = 'RoleBased'


class EntityType(Enum):
	ROLE = 'Role'
	USER = 'User'


@dataclass
class AwsCloudAccountCredentials:
	"""AWS cloud account credentials

		Args:
			arn (str): (Required) AWS Role ARN (to be assumed by Dome9)
			secret (str): (Required) The AWS role External ID (Dome9 will have to use this secret in order to assume the role)
			type (str): (Required) The cloud account onboarding method. Set to "RoleBased".
			api_key (str): (Optional) aws cloud account apiKey.

	"""
	arn: str
	secret: str
	type: str = AwsCloudAccountCredentialsBasedType.ROLE_BASED_TYPE.value
	api_key: str = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		type_options = [type_option.value for type_option in AwsCloudAccountCredentialsBasedType]
		if self.type not in type_options:
			raise UnsupportedCloudAccountCredentialsBasedType(f'base type must be one of the following {type_options}')


@dataclass
class AwsCloudAccountRequest(BaseDataclassRequest):
	"""AWS cloud account request

		Args:
			name (str): (Required) The name of AWS account in Dome9
			credentials (AwsCloudAccountCredentials): (Required) The information needed for Dome9 System in order to connect to the AWS cloud account
			organizational_unit_id (str): (Optional) The Organizational Unit that this cloud account will be attached to

	"""

	name: str
	credentials: AwsCloudAccountCredentials
	organizational_unit_id: str = None


@dataclass
class AwsCloudAccountNetSecRegion:
	"""AWS cloud account net sec region

		Args:
			region (str): (Required) AWS region, in AWS format (e.g., "us-east-1")
			new_group_behavior (str): (Required) The network security configuration. Select "ReadOnly", "FullManage", or "Reset".

	"""
	region: str
	new_group_behavior: str

	@logger.catch(reraise=True)
	def __post_init__(self):
		APIUtils.check_is_valid_aws_region_id(self.region)

		new_group_behaviors = [new_group_behavior.value for new_group_behavior in NewGroupBehaviors]
		if self.new_group_behavior not in new_group_behaviors:
			raise UnsupportedCloudAccountGroupBehaviors(f'new group behaviors must be one of the following {new_group_behaviors}')


@dataclass
class AwsCloudAccountUpdateName(BaseDataclassRequest):
	"""AWS cloud account update name

		Args:
			cloud_account_id (str): (Required) AWS cloud account id
			data (str): (Required) The desired name for aws cloud account

	"""
	cloud_account_id: str
	data: str


@dataclass
class AwsCloudAccountUpdateConfig(BaseDataclassRequest):
	"""AWS cloud account update config

		Args:
			cloud_account_id (str): (Required) AWS cloud account id
			data (AwsCloudAccountNetSecRegion): (Required) AWS cloud account net sec region

	"""
	cloud_account_id: str
	data: AwsCloudAccountNetSecRegion


@dataclass
class AwsCloudAccountUpdateOrganizationalUnitID(BaseDataclassRequest):
	"""AWS cloud account update organizational unit id

		Args:
			organizational_unit_id (str): (Required) The desired organizational unit id to attach to

	"""
	organizational_unit_id: str


@dataclass
class AwsCloudAccountUpdateCredentials(BaseDataclassRequest):
	"""AWS cloud account update credentials

		Args:
			organizational_unit_id (str): (Required) (Required) AWS cloud account id
			data (str): (Required) AWS cloud account credentials

	"""
	cloud_account_id: str
	data: AwsCloudAccountCredentials


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


class AwsCloudAccount(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: AwsCloudAccountRequest) -> Dict:
		"""Create (onboard) aws cloud account

		:param body: Details for the new aws cloud account
		:type body: AwsCloudAccountRequest
		:returns: Dict that has metadata for the created aws cloud account

		"""
		return self._post(route=AwsCloudAccountConsts.MAIN_ROUTE.value, body=body)

	def get(self, aws_cloud_account_id: str) -> Dict:
		"""Get aws cloud account that onboarded to dome9

		:param aws_cloud_account_id: Dome9 aws cloud account id
		:type aws_cloud_account_id: str
		:returns: Dict that has metadata for aws cloud account

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}'
		return self._get(route=route)

	def get_all(self) -> List[Dict]:
		"""Get all aws cloud accounts that already onboarded to dome9

		:returns: List of dicts that has metadata for all the aws cloud accounts

		"""
		return self._get(route=AwsCloudAccountConsts.MAIN_ROUTE.value)

	def update_name(self, body: AwsCloudAccountUpdateName) -> Dict:
		"""Update the name for aws cloud accounts that already onboarded to dome9

		:param body: Details for dome9 aws cloud account
		:type body: AwsCloudAccountUpdateName

		:returns: Dict that has metadata for aws cloud account

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.NAME_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_region_config(self, body: AwsCloudAccountUpdateConfig) -> Dict:
		"""Update the region config for aws cloud accounts that already onboarded to dome9

		:param body: Details for updating the region config of the dome9 aws cloud account
		:type body: AwsCloudAccountUpdateConfig

		:returns: Dict that has metadata for aws cloud account

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.REGION_CONFIG_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_organizational_id(self, aws_cloud_account_id: str, body: AwsCloudAccountUpdateOrganizationalUnitID) -> Dict:
		"""Update the organizational unit id for aws cloud accounts that already onboarded to dome9

		:param aws_cloud_account_id: Dome9 aws cloud account id
		:type aws_cloud_account_id: str
		:param body: Details for aws cloud account in order to update organizational unit id.
		:type body: AwsCloudAccountUpdateOrganizationalUnitID

		:returns: Dict that has metadata for aws cloud account

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsCloudAccountConsts.ORGANIZATIONAL_UNIT_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_credentials(self, body: AwsCloudAccountUpdateCredentials) -> Dict:
		"""Update the credentials for aws cloud accounts that already onboarded to dome9

		:param body: Details for aws cloud account in order to update the credentials.
		:type body: AwsCloudAccountUpdateCredentials

		:returns: Dict that has metadata for aws cloud account

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.CREDENTIALS_ROUTE.value}'
		return self._put(route=route, body=body)

	def delete(self, aws_cloud_account_id: str):
		"""Delete aws cloud account

		:param aws_cloud_account_id: Aws cloud account id
		:type aws_cloud_account_id: str
		:returns: None

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}'
		return self._delete(route=route)

	# attach iam safe to cloud account
	def attach_iam_safe(self, body: AttachIamSafe) -> Dict:
		"""Attach iam safe to aws cloud account

		:param body: Details for aws cloud account in order to attach to iam safe
		:type body: AttachIamSafe
		:returns: Dict that has metadata for attached aws cloud account

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.IAM_SAFE_ROUTE.value}'
		return self._put(route=route, body=body)

	def detach_iam_safe(self, aws_cloud_account_id: str) -> None:
		"""Detach iam safe to aws cloud account

		:param aws_cloud_account_id: Aws cloud account id
		:type aws_cloud_account_id: str
		:returns: Dict that has metadata for attached aws cloud account

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsCloudAccountConsts.IAM_SAFE_ROUTE.value}'
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
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsCloudAccountConsts.RESTRICTED_IAM_ROUTE.value}'
		return self._post(route=route, body=body)

	def get_all_protected_iam_safe_entity(self, aws_cloud_account_id: str) -> Dict:
		"""Get data for all the users and roles

		:param aws_cloud_account_id: Aws security group id.
		:type aws_cloud_account_id: str
		:returns: Dict that has two key, roles and users

		"""
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsCloudAccountConsts.IAM_ENTITIES_ROUTE.value}'
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
		entityTypes = [entityType.value for entityType in EntityType]
		if self.entityType not in entityTypes:
			raise UnsupportedCloudAccountEntityType(f'entity type must be one of the following {entityTypes}')

		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsCloudAccountConsts.RESTRICTED_IAM_ROUTE.value}/{entity_type}'
		return self._delete(route=route, params={AwsCloudAccountConsts.ENTITY_NAME.value: entity_name})

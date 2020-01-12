from dataclasses import dataclass
from enum import Enum
from typing import Dict

from loguru import logger
from dome9.client import Client
from dome9.consts import AwsRegions, NewGroupBehaviors
from dome9.base_dataclass import BaseDataclassRequest
from dome9.exceptions import UnsupportedEntityType

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


class AwsCloudAccountCredentialsConsts(Enum):
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
			apiKey (str): (Optional) aws cloud account apiKey.

	"""
	arn: str
	secret: str
	type: str = AwsCloudAccountCredentialsConsts.ROLE_BASED_TYPE.value
	apiKey: str = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		type_options = [type_option.value for type_option in AwsCloudAccountCredentialsConsts]
		if self.type not in type_options:
			raise ValueError(f'type must be one of the following {type_options}')


@dataclass
class AwsCloudAccountRequest(BaseDataclassRequest):
	"""AWS cloud account request

		Args:
			name (str): (Required) The name of AWS account in Dome9
			credentials (AwsCloudAccountCredentials): (Required) The information needed for Dome9 System in order to connect to the AWS cloud account
			organizationalUnitId (str): (Optional) The Organizational Unit that this cloud account will be attached to

	"""

	name: str
	credentials: AwsCloudAccountCredentials
	organizationalUnitId: str = None


@dataclass
class AwsCloudAccountNetSecRegion:
	"""AWS cloud account net sec region

		Args:
			region (str): (Required) AWS region, in AWS format (e.g., "us-east-1")
			newGroupBehavior (str): (Required) The network security configuration. Select "ReadOnly", "FullManage", or "Reset".

	"""
	region: str
	newGroupBehavior: str

	@logger.catch(reraise=True)
	def __post_init__(self):
		regions = [region.value for region in AwsRegions]
		if self.region not in regions:
			raise ValueError(f'region must be one of the following {regions}')

		new_group_behaviors = [new_group_behavior.value for new_group_behavior in NewGroupBehaviors]
		if self.newGroupBehavior not in new_group_behaviors:
			raise ValueError(f'new group behaviors must be one of the following {new_group_behaviors}')


@dataclass
class AwsCloudAccountUpdateName(BaseDataclassRequest):
	"""AWS cloud account update name

		Args:
			cloudAccountId (str): (Required) AWS cloud account id
			data (str): (Required) The desired name for aws cloud account

	"""
	cloudAccountId: str
	data: str


@dataclass
class AwsCloudAccountUpdateConfig(BaseDataclassRequest):
	"""AWS cloud account update config

		Args:
			cloudAccountId (str): (Required) AWS cloud account id
			data (AwsCloudAccountNetSecRegion): (Required) AWS cloud account net sec region

	"""
	cloudAccountId: str
	data: AwsCloudAccountNetSecRegion


@dataclass
class AwsCloudAccountUpdateOrganizationalUnitID(BaseDataclassRequest):
	"""AWS cloud account update organizational unit id

		Args:
			organizationalUnitId (str): (Required) The desired organizational unit id to attach to

	"""
	organizationalUnitId: str


@dataclass
class AwsCloudAccountUpdateCredentials(BaseDataclassRequest):
	"""AWS cloud account update credentials

		Args:
			cloudAccountId (str): (Required) (Required) AWS cloud account id
			data (str): (Required) AWS cloud account credentials

	"""
	cloudAccountId: str
	data: AwsCloudAccountCredentials


@dataclass
class IAMSafeData:
	"""IAM safe data

		Args:
			awsGroupArn(str): (Required) AWS group arn.
			awsPolicyArn(str): (Required) AWS policy arn.

	"""
	awsGroupArn: str
	awsPolicyArn: str


@dataclass
class AttachIamSafe(BaseDataclassRequest):
	"""IAMSafeData

		Args:
			cloudAccountId(str): (Required) AWS cloud account to attach IAM safe to it.
			data(str): (Required) IAM safe data

	"""
	cloudAccountId: str
	data: IAMSafeData


@dataclass
class RestrictedIamEntitiesRequest(BaseDataclassRequest):
	"""Restricted iam entities request

		Args:
			entityName (str): Aws iam user name or aws role
			entityType (str): Entity type, must be one of the following Role or User

	"""
	entityName: str
	entityType: str

	@logger.catch(reraise=True)
	def __post_init__(self):
		entityTypes = [entityType.value for entityType in EntityType]
		if self.entityType not in entityTypes:
			raise UnsupportedEntityType(f'entity type must be one of the following {entityTypes}')


class AwsCloudAccount(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: AwsCloudAccountRequest):
		return self._post(route=AwsCloudAccountConsts.MAIN_ROUTE.value, body=body)

	def get(self, aws_cloud_account_id: str):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}'
		return self._get(route=route)

	def get_all(self):
		return self._get(route=AwsCloudAccountConsts.MAIN_ROUTE.value)

	def update_name(self, body: AwsCloudAccountUpdateName):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.NAME_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_region_config(self, body: AwsCloudAccountUpdateConfig):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.REGION_CONFIG_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_organizational_id(self, aws_cloud_account_id: str, body: AwsCloudAccountUpdateOrganizationalUnitID):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsCloudAccountConsts.ORGANIZATIONAL_UNIT_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_credentials(self, body: AwsCloudAccountUpdateCredentials):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.CREDENTIALS_ROUTE.value}'
		return self._put(route=route, body=body)

	def delete(self, aws_cloud_account_id: str):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}'
		return self._delete(route=route)

	# attach iam safe to cloud account
	def attach_iam_safe(self, body: AttachIamSafe):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.IAM_SAFE_ROUTE.value}'
		return self._put(route=route, body=body)

	def detach_iam_safe(self, aws_cloud_account_id: str):
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
			raise UnsupportedEntityType(f'entity type must be one of the following {entityTypes}')

		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{aws_cloud_account_id}/{AwsCloudAccountConsts.RESTRICTED_IAM_ROUTE.value}/{entity_type}'
		return self._delete(route=route, params={AwsCloudAccountConsts.ENTITY_NAME.value: entity_name})

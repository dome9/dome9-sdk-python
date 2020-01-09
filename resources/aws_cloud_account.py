from dataclasses import dataclass
from enum import Enum

from loguru import logger
from dome9.client import Client
from dome9.consts import AwsRegions, NewGroupBehaviors
from dome9.base_dataclass import BaseDataclassRequest

from dome9.resource import Dome9Resource


class AwsCloudAccountConsts(Enum):
	MAIN_ROUTE = 'CloudAccounts'
	REGION_CONFIG_ROUTE = 'region-conf'
	ORGANIZATIONAL_UNIT_ROUTE = 'organizationalUnit'
	NAME_ROUTE = 'name'
	CREDENTIALS_ROUTE = 'credentials'
	IAM_SAFE_ROUTE = 'iam-safe'


class AwsCloudAccountCredentialsConsts(Enum):
	USER_BASED_TYPE = 'UserBased'
	ROLE_BASED_TYPE = 'RoleBased'


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
	type: str = AwsCloudAccountCredentialsConsts.ROLE_BASED_TYPE.value
	api_key: str = None

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
		regions = [region.value for region in AwsRegions]
		if self.region not in regions:
			raise ValueError(f'region must be one of the following {regions}')

		new_group_behaviors = [new_group_behavior.value for new_group_behavior in NewGroupBehaviors]
		if self.new_group_behavior not in new_group_behaviors:
			raise ValueError(f'new group behaviors must be one of the following {new_group_behaviors}')


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
			cloud_account_id (str): (Required) (Required) AWS cloud account id
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


class AwsCloudAccount(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: AwsCloudAccountRequest):
		return self._post(route=AwsCloudAccountConsts.MAIN_ROUTE.value, body=body)

	def get(self, awsCloudAccountID: str):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{awsCloudAccountID}'
		return self._get(route=route)

	def get_all(self):
		return self._get(route=AwsCloudAccountConsts.MAIN_ROUTE.value)

	def update_name(self, body: AwsCloudAccountUpdateName):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.NAME_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_region_config(self, body: AwsCloudAccountUpdateConfig):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.REGION_CONFIG_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_organizational_id(self, awsCloudAccountID: str, body: AwsCloudAccountUpdateOrganizationalUnitID):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{awsCloudAccountID}/{AwsCloudAccountConsts.ORGANIZATIONAL_UNIT_ROUTE.value}'
		return self._put(route=route, body=body)

	def update_credentials(self, body: AwsCloudAccountUpdateCredentials):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.CREDENTIALS_ROUTE.value}'
		return self._put(route=route, body=body)

	def delete(self, awsCloudAccountID: str):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{awsCloudAccountID}'
		return self._delete(route=route)

	# attach iam safe to cloud account
	def attach_iam_safe_to_aws_cloud_account(self, body: AttachIamSafe):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.IAM_SAFE_ROUTE.value}'
		return self._put(route=route, body=body)

	def detach_iam_safe_to_aws_cloud_account(self, awsCloudAccountID: str):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{awsCloudAccountID}/{AwsCloudAccountConsts.IAM_SAFE_ROUTE.value}'
		return self._delete(route=route)

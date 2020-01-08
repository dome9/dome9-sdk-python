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
			apiKey (str): (Optional) aws cloud account apiKey.

	"""
	arn: str
	secret: str
	type: str = AwsCloudAccountCredentialsConsts.ROLE_BASED_TYPE.value
	apiKey: str = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		typeOptions = [typeOption.value for typeOption in AwsCloudAccountCredentialsConsts]
		if self.type not in typeOptions:
			raise ValueError(f'type must be one of the following {typeOptions}')


@dataclass
class AwsCloudAccountRequest(BaseDataclassRequest):
	"""AWS cloud account request

		Args:
			name (str): (Required) The name of AWS account in Dome9
			credentials (AwsCloudAccountCredentials): (Required) The information needed for Dome9 System in order to connect to the AWS cloud account
			organizationalUnitID (str): (Optional) The Organizational Unit that this cloud account will be attached to

	"""

	name: str
	credentials: AwsCloudAccountCredentials
	organizationalUnitID: str = None


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
		typeOptions = AwsRegions.values()
		if self.region not in typeOptions:
			raise ValueError(f'region must be one of the following {typeOptions}')

		newGroupBehaviors = NewGroupBehaviors.values()
		if self.newGroupBehavior not in newGroupBehaviors:
			raise ValueError(f'new group behaviors must be one of the following {newGroupBehaviors}')


@dataclass
class AwsCloudAccountUpdateName(BaseDataclassRequest):
	"""AWS cloud account update name

		Args:
			cloudAccountID (str): (Required) AWS cloud account id
			data (str): (Required) The desired name for aws cloud account

	"""
	cloudAccountID: str
	data: str


@dataclass
class AwsCloudAccountUpdateConfig(BaseDataclassRequest):
	"""AWS cloud account update config

		Args:
			cloudAccountID (str): (Required) AWS cloud account id
			data (AwsCloudAccountNetSecRegion): (Required) AWS cloud account net sec region

	"""
	cloudAccountID: str
	data: AwsCloudAccountNetSecRegion


@dataclass
class AwsCloudAccountUpdateOrganizationalUnitID(BaseDataclassRequest):
	"""AWS cloud account update organizational unit id

		Args:
			organizationalUnitID (str): (Required) The desired organizational unit id to attach to

	"""
	organizationalUnitID: str


@dataclass
class AwsCloudAccountUpdateCredentials(BaseDataclassRequest):
	"""AWS cloud account update credentials

		Args:
			cloudAccountId (str): (Required) (Required) AWS cloud account id
			AwsCloudAccountCredentials (str): (Required) AWS cloud account credentials

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
			cloudAccountID(str): (Required) AWS cloud account to attach IAM safe to it.
			data(str): (Required) IAM safe data

	"""
	cloudAccountID: str
	data: IAMSafeData


class AwsCloudAccount(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: AwsCloudAccountRequest):
		return self._post(route=AwsCloudAccountConsts.MAIN_ROUTE.value, body=body)

	def get(self, awsCloudAccountID: str):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{awsCloudAccountID}'
		return self._get(route=route)

	def getAll(self):
		return self._get(route=AwsCloudAccountConsts.MAIN_ROUTE.value)

	def updateName(self, body: AwsCloudAccountUpdateName):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.NAME_ROUTE.value}'
		return self._put(route=route, body=body)

	def updateRegionConfig(self, body: AwsCloudAccountUpdateConfig):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.REGION_CONFIG_ROUTE.value}'
		return self._put(route=route, body=body)

	def updateOrganizationalID(self, awsCloudAccountID: str, body: AwsCloudAccountUpdateOrganizationalUnitID):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{awsCloudAccountID}/{AwsCloudAccountConsts.ORGANIZATIONAL_UNIT_ROUTE.value}'
		return self._put(route=route, body=body)

	def updateCredentials(self, body: AwsCloudAccountUpdateCredentials):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.CREDENTIALS_ROUTE.value}'
		return self._put(route=route, body=body)

	def delete(self, awsCloudAccountID: str):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{awsCloudAccountID}'
		return self._delete(route=route)

	# attach iam safe to cloud account
	def attachIAMSafeToAWSCloudAccount(self, body: AttachIamSafe):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{AwsCloudAccountConsts.IAM_SAFE_ROUTE.value}'
		return self._put(route=route, body=body)

	def detachIAMSafeToAWSCloudAccount(self, awsCloudAccountID: str):
		route = f'{AwsCloudAccountConsts.MAIN_ROUTE.value}/{awsCloudAccountID}/{AwsCloudAccountConsts.IAM_SAFE_ROUTE.value}'
		return self._delete(route=route)

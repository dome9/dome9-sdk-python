from dataclasses import dataclass
from enum import Enum

from loguru import logger
from dome9.client import Client
from dome9.consts import AwsRegions, NewGroupBehaviors
from dome9.dome9_base_dataclass import BaseDataclassRequest

from dome9.dome9_resource import Dome9Resource


class AwsCloudAccountConsts(Enum):
	MAIN_ROUTE = 'CloudAccounts'
	REGION_CONFIG_ROUTE = 'region-conf'
	ORGANIZATIONAL_UNIT_ROUTE = 'organizationalUnit'
	NAME_ROUTE = 'name'
	CREDENTIALS_ROUTE = 'credentials'


class AwsCloudAccountCredentialsConsts(Enum):
	USER_BASED_TYPE = 'UserBased'
	ROLE_BASED_TYPE = 'RoleBased'


@dataclass
class AwsCloudAccountCredentials:
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
	name: str
	credentials: AwsCloudAccountCredentials
	FullProtection: bool = None
	allowReadOnly: bool = None
	organizationalUnitID: str = None
	organizationalUnitPath: str = None
	organizationalUnitName: str = None
	lambdaScanner: bool = None


@dataclass
class AwsCloudAccountNetSecRegion:
	region: str
	newGroupBehavior: str
	name: str = None

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
	cloudAccountID: str
	# data is the name of the aws cloud account
	data: str


@dataclass
class AwsCloudAccountUpdateConfig(BaseDataclassRequest):
	cloudAccountID: str
	data: AwsCloudAccountNetSecRegion


@dataclass
class AwsCloudAccountUpdateOrganizationalUnitID(BaseDataclassRequest):
	organizationalUnitID: str


@dataclass
class AwsCloudAccountUpdateCredentials(BaseDataclassRequest):
	cloudAccountId: str
	data: AwsCloudAccountCredentials


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

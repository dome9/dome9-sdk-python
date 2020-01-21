from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union

from loguru import logger

from dome9 import BaseDataclassRequest, APIUtils, Dome9Resource, Client
from dome9.consts import NewGroupBehaviors
from dome9.exceptions import UnsupportedCloudAccountCredentialsBasedType, UnsupportedCloudAccountGroupBehaviors


class AwsCloudAccountConsts(Enum):
	CLOUD_ACCOUNTS = 'CloudAccounts'
	REGION_CONFIG = 'region-conf'
	ORGANIZATIONAL_UNIT = 'organizationalUnit'
	NAME = 'name'
	CREDENTIALS = 'credentials'


class AwsCloudAccountCredentialsBasedType(Enum):
	USER_BASED = 'UserBased'
	ROLE_BASED = 'RoleBased'


@dataclass
class CloudAccountCredentials:
	"""The information needed for Dome9 System in order to connect to the AWS cloud account

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountcredentialsviewmodel
	:param arn: [Required] AWS Role ARN (to be assumed by Dome9 System)
	:type  arn: str
	:param secret: [Required] The AWS role External ID (Dome9 System will have to use this secret in order to assume the role)
	:type  secret: str
	:param type: [Required] The cloud account onbiarding method. Should be set to "RoleBased" as other methods are deprecated
	:type  type str

	"""
	arn: str
	secret: str
	type: str = AwsCloudAccountCredentialsBasedType.ROLE_BASED.value

	@logger.catch(reraise=True)
	def __post_init__(self):
		type_options = [type_option.value for type_option in AwsCloudAccountCredentialsBasedType]
		if self.type not in type_options:
			raise UnsupportedCloudAccountCredentialsBasedType(f'base type must be one of the following {type_options}')


@dataclass
class CloudAccount(BaseDataclassRequest):
	"""The new AWS account data

	:link https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
	:param name: The cloud account name
	:type name: str
	:param credentials: [Required] The information needed for Dome9 System in order to connect to the AWS cloud account
	:type credentials: CloudAccountCredentials
	:param organizational_unit_id:
	:type organizational_unit_id: str

	"""

	name: str
	credentials: CloudAccountCredentials
	organizational_unit_id: str = None


@dataclass
class CloudAccountRegionConfiguration:
	"""AWS cloud account net sec region

	:link https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountregionconfigurationviewmodel
	:param region: Dome9 representation value for the AWS region
	:type region: str
	:param new_group_behavior: The Protection Mode that Dome9 will apply to new security groups detected in the cloud account. ReadOnly New Security Groups will be included in Dome9 in Read-Only mode, without changes to any of the rules FullManage New Security Groups will be included in Dome9 in Full Protection mode, without changes to any of the rules Reset New Security Groups will be included in Dome9 in Full Protection mode, and all inbound and outbound rules will be cleared
	:type new_group_behavior: str


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

	:link  https://api-v2-docs.dome9.com/#cloudaccounts_updatecloudaccountname
	:param cloud_account_id:
	:type  cloud_account_id: str
	:param data:the new name for the account
	:type  data: str

	"""
	cloud_account_id: str
	data: str


@dataclass
class CloudAccountRegionConfigurationViewModel(BaseDataclassRequest):
	"""AWS cloud account update config

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountpartialupdateviewmodel_dome9-web-api-models-cloudaccountregionconfigurationviewmodel_
	:param cloud_account_id: The Dome9 cloud account id, at least one of the following properties must be provided: "cloudAccountId", "externalAccountNumber"
	:type  cloud_account_id: str
	:param data:
	:type  data: CloudAccountRegionConfiguration

	"""
	cloud_account_id: str
	data: CloudAccountRegionConfiguration


@dataclass
class CloudAccountUpdateOrganizationalUnitId(BaseDataclassRequest):
	"""AWS cloud account update organizational unit id

	:link https://api-v2-docs.dome9.com/#cloudaccounts_updateorganziationalid
	:param organizational_unit_id: The Guid ID of the Organizational Unit to attach to. Use 'null' to attach to the root Organizational Unit
	:type  organizational_unit_id: str

	"""
	organizational_unit_id: str


@dataclass
class CloudAccountCredentialsViewModel(BaseDataclassRequest):
	"""AWS cloud account update credentials

	:link https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountpartialupdateviewmodel_dome9-web-api-models-cloudaccountcredentialsviewmodel_
	:param cloud_account_id: The Dome9 cloud account id
	:type  cloud_account_id: str
	:param data:
	:type  data: CloudAccountCredentials

	"""
	cloud_account_id: str
	data: CloudAccountCredentials


class AwsCloudAccount(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: CloudAccount) -> Dict:
		"""Create (onboard) aws cloud account

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_post
		:param   body: Details for the new aws cloud account
		:type    body: CloudAccount
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype   CloudAccount

		"""
		return self._post(route=AwsCloudAccountConsts.CLOUD_ACCOUNTS.value, body=body)

	def get(self, aws_cloud_account_id: str = '') -> Union[Dict, List[Dict]]:
		"""Fetch a specific AWS cloud account

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_get
		:param   aws_cloud_account_id: Dome9 aws cloud account id
		:type    aws_cloud_account_id: str
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype    CloudAccount

		"""
		route = f'{AwsCloudAccountConsts.CLOUD_ACCOUNTS.value}/{aws_cloud_account_id}'
		return self._get(route=route)

	def update_cloud_account_name(self, body: AwsCloudAccountUpdateName) -> Dict:
		"""Update an AWS cloud account name

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_updatecloudaccountname
		:param   body: Details for dome9 aws cloud account
		:type    body: AwsCloudAccountUpdateName
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype   CloudAccount

		"""
		route = f'{AwsCloudAccountConsts.CLOUD_ACCOUNTS.value}/{AwsCloudAccountConsts.NAME.value}'
		return self._put(route=route, body=body)

	def update_region_config(self, body: CloudAccountRegionConfigurationViewModel) -> Dict:
		"""Update an AWS cloud account region configuration

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_updatecloudaccountregionconf
		:param   body: updated Regional Configuration parameters for the account
		:type    body: CloudAccountRegionConfigurationViewModel
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype   CloudAccount

		"""
		route = f'{AwsCloudAccountConsts.CLOUD_ACCOUNTS.value}/{AwsCloudAccountConsts.REGION_CONFIG.value}'
		return self._put(route=route, body=body)

	def update_organizational_id(self, aws_cloud_account_id: str, body: CloudAccountUpdateOrganizationalUnitId) -> Dict:
		"""Update the ID of the Organizational Unit that this cloud account will be attached to. Use 'null' for the root Organizational Unit

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_updateorganziationalid
		:param   aws_cloud_account_id: The Dome9 Guid ID of the AWS cloud account
		:type    aws_cloud_account_id: str
		:param   body: The Guid ID of the Organizational Unit to attach to. Use 'null' to attach to the root Organizational Unit
		:type    body: CloudAccountUpdateOrganizationalUnitId
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype   CloudAccount

		"""
		route = f'{AwsCloudAccountConsts.CLOUD_ACCOUNTS.value}/{aws_cloud_account_id}/{AwsCloudAccountConsts.ORGANIZATIONAL_UNIT.value}'
		return self._put(route=route, body=body)

	def update_credentials(self, body: CloudAccountCredentialsViewModel) -> Dict:
		"""Update credentials for an AWS cloud account in Dome9. At least one of the following properties must be provided: "cloudAccountId", "externalAccountNumber"

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_updatecloudaccountcredentials
		:param   body: credentials block
		:type    body: CloudAccountCredentialsViewModel
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype   CloudAccount

		"""
		route = f'{AwsCloudAccountConsts.CLOUD_ACCOUNTS.value}/{AwsCloudAccountConsts.CREDENTIALS.value}'
		return self._put(route=route, body=body)

	def delete(self, aws_cloud_account_id: str):
		"""Delete an AWS cloud account

		:link https://api-v2-docs.dome9.com/#cloudaccounts_delete
		:param aws_cloud_account_id: The Dome9 AWS account id (UUID)
		:type aws_cloud_account_id: str
		:returns: None

		"""
		route = f'{AwsCloudAccountConsts.CLOUD_ACCOUNTS.value}/{aws_cloud_account_id}'
		return self._delete(route=route)

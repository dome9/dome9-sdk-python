from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Union
from loguru import logger
from dome9 import BaseDataclassRequest, Dome9Resource, Client, APIUtils
from dome9.exceptions import UnsupportedProtectionMode, UnsupportedPolicyType


class AWSSecurityGroupConsts(Enum):
	CLOUD_SECURITY_GROUP = 'CloudSecurityGroup'
	PROTECTION_MODE = 'protection-mode'
	SERVICES = 'services'


class ProtectionModeConsts(Enum):
	FULL_MANAGE = 'FullManage'
	READ_ONLY = 'ReadOnly'


class PolicyTypeConsts(Enum):
	IN_POUND = 'Inbound'
	OUT_BOUND = 'Outbound'


@dataclass
class ScopeElement:
	"""

	:link  https://api-v2-docs.dome9.com/#schemafalconetix-webapi-models-scopeelementviewmodel
	:param type:
	:type  type: str
	:param data:
	:type  data: Dict

	"""
	type: str
	data: Dict


@dataclass
class CloudSecurityGroupService(BaseDataclassRequest):
	"""Details for a security group service

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudsecuritygroupserviceviewmodel
	:param name:
	:type  name: str
	:param protocolType: Service Protocol
	:type  protocolType: str
	:param description:
	:type  description: str
	:param port: indicates a port range
	:type  port: str
	:param openForAll: indicates the service is open to all ports
	:type  openForAll: bool
	:param scope: List of scopes for the service (CIDR / DNS / AWS Security group / IP List / Magic IP)
	:type  scope: List[ScopeElement]

	"""
	name: str
	protocolType: str
	description: str = None
	port: str = None
	openForAll: bool = None
	scope: List[ScopeElement] = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		APIUtils.check_is_valid_protocol(protocol=self.protocolType)


@dataclass
class Services:
	"""

	:param inbound:
	:type  inbound: List[CloudSecurityGroupService]
	:param outbound:
	:type  outbound: List[CloudSecurityGroupService]

	"""
	inbound: List[CloudSecurityGroupService]
	outbound: List[CloudSecurityGroupService]


@dataclass
class CloudSecurityGroup(BaseDataclassRequest):
	"""Details for the new AWS security group

	:link https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudsecuritygroupviewmodel
	:param securityGroupName:
	:type securityGroupName: str
	:param cloudAccountId:
	:type cloudAccountId: str
	:param regionId:
	:type regionId: str
	:param description:
	:type description: str
	:param isProtected: Note: to set the protection mode, first create the Security Group, then update it with the desired protection mode value ('true' for Protected).
	:type isProtected: bool
	:param vpcId:
	:type vpcId: str
	:param vpcName:
	:type vpcName: str
	:param services:
	:type services: Services
	:param tags:
	:type tags: Dict

	"""
	securityGroupName: str
	cloudAccountId: str
	regionId: str
	description: str = None
	isProtected: bool = None
	vpcId: str = None
	vpcName: str = None
	services: Services = None
	tags: Dict = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		APIUtils.check_is_valid_aws_region_id(region=self.regionId)


@dataclass
class CloudSecurityGroupProtectionModeChange(BaseDataclassRequest):
	"""

	:link https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudsecuritygroupprotectionmodechangeviewmodel
	:param protection_mode:
	:type protection_mode: str

	"""
	protection_mode: str

	@logger.catch(reraise=True)
	def __post_init__(self):
		protection_modes = [protection_mode.value for protection_mode in ProtectionModeConsts]
		if self.protection_mode not in protection_modes:
			raise UnsupportedProtectionMode(f'protection mode must be one of the following {protection_modes}')


class AwsSecurityGroup(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: CloudSecurityGroup) -> Dict:
		"""Create aws security group

		:link https://api-v2-docs.dome9.com/#cloudsecuritygroup_createcloudsecuritygroup
		:param body: Details for the new aws security group
		:type body: CloudSecurityGroup
		:returns: Dict that has metadata for the created aws security group

		"""
		return self._post(route=AWSSecurityGroupConsts.CLOUD_SECURITY_GROUP.value, body=body)

	def get(self, security_group_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get aws security group

		:link   https://api-v2-docs.dome9.com/#cloudsecuritygroup_get
		:param  security_group_id: Dome9 aws security group id
		:type   security_group_id: str
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudsecuritygroupviewmodel
		:rtype  CloudSecurityGroup

		"""
		route = f'{AWSSecurityGroupConsts.CLOUD_SECURITY_GROUP.value}/{security_group_id}'
		return self._get(route=route)

	def get_all_in_region(self, cloud_account_id: str, region_id: str) -> List[Dict]:
		"""Get aws security groups for a specific cloud account and region

		:link   https://api-v2-docs.dome9.com/#cloudsecuritygroup_get
		:param  cloud_account_id: the cloud account id
		:type   cloud_account_id: str
		:param  region_id: the region
		:type   region_id: str
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudsecuritygroupviewmodel
		:rtype  List[CloudSecurityGroup]

		"""
		query_parameters = {'cloudAccountId': cloud_account_id, 'regionId': region_id}
		return self._get(route=AWSSecurityGroupConsts.CLOUD_SECURITY_GROUP.value, params=query_parameters)


	def update(self, security_group_id: str, body: CloudSecurityGroup) -> None:
		"""Updates an AWS security group protection mode

		:link  https://api-v2-docs.dome9.com/#cloudsecuritygroup_updatesecgroup
		:param security_group_id: the AWS security group id
		:type  security_group_id: str
		:param body: updated details for the security group. only 'IsProtected' is used in this call which defines whether to protect or unprotect the security group.
		:type  body: CloudSecurityGroup

		"""
		route = f'{AWSSecurityGroupConsts.CLOUD_SECURITY_GROUP.value}/{security_group_id}'
		return self._put(route=route, body=body)

	def change_protection_mode(self, security_group_id: str, body: CloudSecurityGroupProtectionModeChange) -> Dict:
		"""Change the protection mode for an AWS security group

		:link https://api-v2-docs.dome9.com/#cloudsecuritygroup_changeprotectionmode
		:param security_group_id: the AWS security group id (Dome9 internal ID / AWS security group ID)
		:type security_group_id: str
		:param body: details for the security group, including the protection mode. Only 'ProtectionMode' is required in this call (FullManage or ReadOnly).
		:type body: CloudSecurityGroupProtectionModeChange
		:return metadata
		:rtype Dict

		"""
		route = f'{AWSSecurityGroupConsts.CLOUD_SECURITY_GROUP.value}/{security_group_id}/{AWSSecurityGroupConsts.PROTECTION_MODE.value}'
		return self._post(route=route, body=body)

	def update_security_group_service(self, security_group_id: str, policy_type: str, body: CloudSecurityGroupService) -> Dict:
		"""Update a service (rule) for an AWS security group

		:link https://api-v2-docs.dome9.com/#cloudsecuritygroup_updateserviceforcloudtosecuritygroup
		:param security_group_id: Aws security group id.
		:type security_group_id: str
		:param policy_type: The service type (Inbound / Outbound)
		:type policy_type: str
		:param body: Updated details for the service
		:type body: CloudSecurityGroupService
		:returns: Dict that has metadata for the updated security group

		"""
		policy_types = [policy_type.value for policy_type in PolicyTypeConsts]
		if policy_type not in policy_types:
			raise UnsupportedPolicyType(f'policy type must be one of the following {policy_types}')

		route = f'{AWSSecurityGroupConsts.CLOUD_SECURITY_GROUP.value}/{security_group_id}/{AWSSecurityGroupConsts.SERVICES.value}/{policy_type}'
		return self._post(route=route, body=body)

	def delete(self, security_group_id: str) -> None:
		"""Delete aws security group

		:link https://api-v2-docs.dome9.com/#cloudsecuritygroup_deletecloudsecuritygroup
		:param security_group_id: Aws security group id.
		:type security_group_id: str
		:returns: None

		"""
		route = f'{AWSSecurityGroupConsts.CLOUD_SECURITY_GROUP.value}/{security_group_id}'
		return self._delete(route=route)

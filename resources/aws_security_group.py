from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
from loguru import logger
from dome9 import APIUtils
from dome9 import BaseDataclassRequest, Dome9Resource, Client
from dome9.exceptions import UnsupportedProtectionMode, UnsupportedPolicyType


class AWSSecurityGroupConsts(Enum):
	SECURITY_GROUP_ROUTE = 'CloudSecurityGroup'
	PROTECTION_MODE_ROUTE = 'protection-mode'
	SERVICES_ROUTE = 'services'


class ProtectionModeConsts(Enum):
	FULL_MANAGE = 'FullManage'
	READ_ONLY = 'ReadOnly'


class PolicyTypeConsts(Enum):
	IN_POUND = 'Inbound'
	OUT_BOUND = 'Outbound'


@dataclass
class Scope:
	"""Service scope
		Args:
			type (str): (Required) scope type
			data (Dict): (Required) scope data

	"""
	type: str
	data: Dict


@dataclass
class BoundServices(BaseDataclassRequest):
	"""Bound services

		Args:
			name (str): (Required) Service name.
			protocolType (str): (Required) Service protocol type.
			description (str): (Optional) Service description
			port (str): (Optional) Service type (port).
			openForAll (bool): (Optional) Is open for all.
			scope (Scope): (Optional) Service scope

	"""
	name: str
	protocolType: str
	description: str = None
	port: str = None
	openForAll: bool = None
	scope: List[Scope] = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		APIUtils.check_is_valid_protocol(protocol=self.protocolType)


@dataclass
class Services:
	"""AWS security group request

		Args:
			inbound (BoundServices): (Required) inbound service.
			outbound (BoundServices): (Required) outbound service.

	"""
	inbound: List[BoundServices]
	outbound: List[BoundServices]


@dataclass
class AwsSecurityGroupRequest(BaseDataclassRequest):
	"""AWS security group request

		Args:
			securityGroupName (str): (Required) Name of the Security Group
			cloudAccountId (str): (Required) Cloud account id in Dome9
			regionId (str): (Required) AWS region, in AWS format (e.g., "us-east-1"); default is us_east_1
			description (str): (Optional) Security Group description
			isProtected (bool): (Optional) Indicates the Security Group is in Protected mode.
				Note: to set the protection mode, first create the Security Group, then update it with the desired protection mode value ('true' for Protected).
			vpcId (str): (Optional) VPC id for VPC containing the Security Group.
			vpcName (str): (Optional) Security Group VPC name.
			services (Services): (Optional) Security Group services.
			tags (Dict): (Optional) Security Group tags.

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
class GetSecurityGroupParameters(BaseDataclassRequest):
	"""AWS security group request

		Args:
			cloudAccountId (str): (Required) AWS cloud account Id
			regionId (str): (Required) AWS region, in AWS format (e.g., "us-east-1"); default is us_east_1

	"""
	cloud_account_id: str
	region_id: str

	@logger.catch(reraise=True)
	def __post_init__(self):
		APIUtils.check_is_valid_aws_region_id(region=self.region_id)


@dataclass
class UpdateSecurityGroupProtectionModeParameters(BaseDataclassRequest):
	"""AWS security group request

		Args:
			protectionMode (str): (Required) AWS region, in AWS format (e.g., "us-east-1"); default is us_east_1

	"""
	protectionMode: str

	@logger.catch(reraise=True)
	def __post_init__(self):
		protection_modes = [protection_mode.value for protection_mode in ProtectionModeConsts]
		if self.protectionMode not in protection_modes:
			raise UnsupportedProtectionMode(f'protection mode must be one of the following {protection_modes}')


class AwsSecurityGroup(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: AwsSecurityGroupRequest) -> Dict:
		"""Create aws security group

		:param body: Details for the new AWS security group
		:type body: AwsSecurityGroupRequest
		:returns: Dict that has metadata for the created aws security group

		"""
		return self._post(route=AWSSecurityGroupConsts.SECURITY_GROUP_ROUTE.value, body=body)

	def get(self, security_group_id: str) -> Dict:
		"""Get aws security group

		:param security_group_id: Dome9 aws security group id
		:type security_group_id: str
		:returns: Dict that has metadata for the aws security group

		"""
		route = f'{AWSSecurityGroupConsts.SECURITY_GROUP_ROUTE.value}/{security_group_id}'
		return self._get(route=route)

	def get_all_in_region(self, body: GetSecurityGroupParameters) -> List[Dict]:
		"""Get AWS security groups for a specific cloud account and region

		:param body: Details for the getting all the security groups in a specific region
		:type body: GetSecurityGroupParameters
		:returns: List of dicts that has metadata for all the aws security groups in specific region

		"""
		return self._get(route=AWSSecurityGroupConsts.SECURITY_GROUP_ROUTE.value, body=body)

	def get_all(self) -> List[Dict]:
		"""Get all aws security group

		:returns: List of dicts that has metadata for all the aws security groups

		"""
		return self._get(route=AWSSecurityGroupConsts.SECURITY_GROUP_ROUTE.value)

	def update(self, security_group_id: str, body: AwsSecurityGroupRequest) -> Dict:
		"""Update aws security group, in order to update the field isProtected update_protection_mode function should be called

		:param security_group_id: Aws security group id.
		:type security_group_id: str
		:param body: Details for updating the security group
		:type body: AwsSecurityGroupRequest
		:returns: Dict that has metadata for the updated security group

		"""
		route = f'{AWSSecurityGroupConsts.SECURITY_GROUP_ROUTE.value}/{security_group_id}'
		return self._put(route=route, body=body)

	def update_protection_mode(self, security_group_id: str, body: UpdateSecurityGroupProtectionModeParameters) -> Dict:
		"""Update aws security group protection mode

		:param security_group_id: Aws security group id.
		:type security_group_id: str
		:param body: Details for updating protection mode
		:type body: UpdateSecurityGroupProtectionModeParameters
		:returns: Dict that has metadata for the updated security group

		"""
		route = f'{AWSSecurityGroupConsts.SECURITY_GROUP_ROUTE.value}/{security_group_id}/{AWSSecurityGroupConsts.PROTECTION_MODE_ROUTE.value}'
		return self._post(route=route, body=body)

	def handle_bound_services(self, security_group_id: str, policy_type: str, body: BoundServices) -> Dict:
		"""Create and attach or update bound service

		:param security_group_id: Aws security group id.
		:type security_group_id: str
		:param policy_type: The service type (Inbound / Outbound)
		:type policy_type: str
		:param body: Updated details for the service
		:type body: BoundServices
		:returns: Dict that has metadata for the updated security group

		"""
		policy_types = [policy_type.value for policy_type in PolicyTypeConsts]
		if policy_type not in policy_types:
			raise UnsupportedPolicyType(f'policy type must be one of the following {policy_types}')

		route = f'{AWSSecurityGroupConsts.SECURITY_GROUP_ROUTE.value}/{security_group_id}/{AWSSecurityGroupConsts.SERVICES_ROUTE.value}/{policy_type}'
		return self._post(route=route, body=body)

	def delete(self, security_group_id: str) -> None:
		"""Delete aws security group

		:param security_group_id: Aws security group id.
		:type security_group_id: str
		:returns: None

		"""
		route = f'{AWSSecurityGroupConsts.SECURITY_GROUP_ROUTE.value}/{security_group_id}'
		return self._delete(route=route)

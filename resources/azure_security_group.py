from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from loguru import logger

from dome9 import BaseDataclassRequest, Dome9Resource, Client, APIUtils


class AzureSecurityGroupConsts(Enum):
	MAIN_ROUTE = 'AzureSecurityGroupPolicy'


@dataclass
class AzureSecurityGroupScope(BaseDataclassRequest):
	"""Azure security group scope

		Args:
			type (str): (Required) scope type
			data (Dict): (Required) scope data

	"""
	type: str
	data: Dict


@dataclass
class AzureSecurityGroupBoundService(BaseDataclassRequest):
	"""Azure Security Group create request

			Args:
				name (str): (Required) Service name
				priority (int): (Required) Service priority (a number between 100 and 4096)
				protocol (str): (Required) Service protocol (UDP / TCP / ANY)
				source_port_ranges (List[str]): (Required) Source port ranges
				source_scopes (List[AzureSecurityGroupScope]): (Required) List of source scopes for the service (CIDR / IP List / Tag)
				destination_port_ranges (List[str]): (Required) Destination port ranges
				destination_scopes (List[AzureSecurityGroupScope]): (Required) List of destination scopes for the service (CIDR / IP List / Tag)
				is_default (bool): Gets or sets the default security rules of network security group
				access (str): (Required) Service access (Allow / Deny)
				direction (str): (Required) Inbound/Outbound
				description (str): (Optional) Service description

	"""
	name: str
	priority: int
	protocol: str
	source_port_ranges: List[str]
	source_scopes: List[AzureSecurityGroupScope]
	destination_port_ranges: List[str]
	destination_scopes: List[AzureSecurityGroupScope]
	access: str
	direction: str
	is_default: bool = None
	description: str = None

	def __post_init__(self):
		APIUtils.check_is_valid_priority(self.priority)
		APIUtils.check_is_valid_protocol(self.protocol)
		APIUtils.check_is_valid_access(self.access)
		APIUtils.check_is_valid_direction(self.direction)


@dataclass
class AzureSecurityGroupRequest(BaseDataclassRequest):
	"""Azure Security Group create request

			Args:
				name (str): (Required) Name of the security group
				region (str): (Required) Azure region can be one of the following: centralus, eastus, eastus2, usgovlowa, usgovvirginia, northcentralus, southcentralus, westus, westus2, westcentralus, northeurope, westeurope, eastasia, southeastasia, japaneast, japanwest, brazilsouth, australiaeast, australiasoutheast, centralindia, southindia, westindia, chinaeast, chinanorth, canadacentral, canadaeast, germanycentral, germanynortheast, koreacentral, uksouth, ukwest, koreasout
				resource_group (str): (Required) Azure resource group name
				cloud_account_id (str): (Required) Cloud account id in Dome9
				inbound_services (List[AzureSecurityGroupBoundService]): (Optional) Security group services
				outbound_services (List[AzureSecurityGroupBoundService]): (Optional) Security group services
				is_tamper_protected (bool): (Optional) Is security group tamper protected
				description (str): (Optional) Security group description
				tags (Dict): (Optional) Security group tags

	"""
	name: str
	region: str
	resource_group: str
	cloud_account_id: str
	inbound_services: List[AzureSecurityGroupBoundService] = None
	outbound_services: List[AzureSecurityGroupBoundService] = None
	is_tamper_protected: bool = None
	description: str = None
	tags: Dict = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		APIUtils.check_is_valid_azure_region(region=self.region)


class AzureSecurityGroup(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: AzureSecurityGroupRequest) -> Dict:
		"""Creates Azure Security Group

		:param body: Azure Security Group request payload
		:return: Response dict

		"""
		return self._post(route=AzureSecurityGroupConsts.MAIN_ROUTE.value, body=body)

	def get(self, azure_security_group_id: str) -> Dict:
		"""Get Azure Security Group by ID

		:param azure_security_group_id: Azure Security Group ID
		:return: Response dict

		"""
		route = f'{AzureSecurityGroupConsts.MAIN_ROUTE.value}/{azure_security_group_id}'
		return self._get(route=route)

	def get_all(self) -> List[Dict]:
		"""Get all Azure Security Groups

		:return: List of response dicts

		"""
		return self._get(route=AzureSecurityGroupConsts.MAIN_ROUTE.value)

	def update(self, azure_security_group_id: str, body: AzureSecurityGroupRequest) -> Dict:
		"""Updates existing Azure Security Group

		:param azure_security_group_id: Azure Security Group ID
		:param body: Azure Security Group request payload
		:return: Response dict

		"""
		route = f'{AzureSecurityGroupConsts.MAIN_ROUTE.value}/{azure_security_group_id}'
		return self._put(route=route, body=body)

	def delete(self, azure_security_group_id: str) -> None:
		"""Deletes Azure Security Group

		:param azure_security_group_id: Azure Security Group ID
		:return: None

		"""
		route = f'{AzureSecurityGroupConsts.MAIN_ROUTE.value}/{azure_security_group_id}'
		return self._delete(route=route)

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union

from loguru import logger

from dome9 import BaseDataclassRequest, Dome9Resource, Client, APIUtils


class AzureSecurityGroupConsts(Enum):
	AZURE_SECURITY_GROUP_POLICY = 'AzureSecurityGroupPolicy'


@dataclass
class AzureSecurityGroupScope(BaseDataclassRequest):
	"""Azure security group scope

	:link  https://api-v2-docs.dome9.com/index.html?python#schemafalconetix-webapi-models-scopeelementviewmodel
	:param type: Scope type
	:type  type: str
	:param data: Scope data
	:type  data: Dict
	"""
	type: str
	data: Dict


@dataclass
class AzureSecurityGroupBoundService(BaseDataclassRequest):
	"""

	:link  https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-azure-securitygrouppolicy-viewmodels-azuresgpolicyserviceviewmodel
	:param name: Service name
	:type  name: str
	:param priority: Service priority (a number between 100 and 4096)
	:type  priority: int
	:param protocol: Service protocol (UDP / TCP / ANY)
	:type  protocol: str
	:param source_port_ranges: Source port ranges
	:type  source_port_ranges: List[str]
	:param source_scopes: List of source scopes for the service (CIDR / IP List / Tag)
	:type  source_scopes: List[AzureSecurityGroupScope]
	:param destination_port_ranges: Destination port ranges
	:type  destination_port_ranges: List[str]
	:param destination_scopes: List of destination scopes for the service (CIDR / IP List / Tag)
	:type  destination_scopes:List[AzureSecurityGroupScope]
	:param is_default
	:type  is_default: bool
	:param access: Service access (Allow / Deny)
	:type  access: str
	:param direction: Inbound/Outbound
	:type  direction: str
	:param description: Service description
	:type  description: str
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
	"""Create a security group policy

	:link  https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-azure-securitygrouppolicy-viewmodels-azuresgpolicypostviewmodel
	:param name: Policy name
	:type  name: str
	:param region: Policy region
	:type  region: str
	:param resource_group: Azure resource group name
	:type  resource_group: str
	:param cloud_account_id: Cloud account id in Dome9
	:type  cloud_account_id: str
	:param inbound_services: Security group services
	:type  inbound_services: List[AzureSecurityGroupBoundService]
	:param outbound_services: Security group services
	:type  outbound_services: List[AzureSecurityGroupBoundService]
	:param is_tamper_protected: Policy is tamper protected
	:type  is_tamper_protected: bool
	:param description: Policy description
	:type  description: str
	:param tags: Security group tags
	:type  tags: Dict

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

		:link   https://api-v2-docs.dome9.com/index.html?python#azuresecuritygrouppolicy_post
		:param  body: Azure Security Group request payload
		:type   body: AzureSecurityGroupRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-azure-securitygrouppolicy-viewmodels-azuresgpolicygetviewmodel
		:rtype  AzureSgPolicyGet

		"""
		return self._post(route=AzureSecurityGroupConsts.AZURE_SECURITY_GROUP_POLICY.value, body=body)

	def get(self, azure_security_group_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get Network Security Group Policies for the Azure accounts in the Dome9 account

		:link   https://api-v2-docs.dome9.com/index.html?python#azuresecuritygrouppolicy_get
		:param  azure_security_group_id: Dome9 azure security Group ID
		:param  azure_security_group_id: str
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-azure-securitygrouppolicy-viewmodels-azuresgpolicygetviewmodel
		:rtype  AzureSgPolicyGet

		"""
		route = f'{AzureSecurityGroupConsts.AZURE_SECURITY_GROUP_POLICY.value}/{azure_security_group_id}'
		return self._get(route=route)

	def update(self, azure_security_group_id: str, body: AzureSecurityGroupRequest) -> Dict:
		"""Updates existing Azure Security Group

		:link   https://api-v2-docs.dome9.com/index.html?python#azuresecuritygrouppolicy_put
		:param  azure_security_group_id: Azure Security Group ID
		:param  azure_security_group_id: str
		:type   body: Details for the policy, including the changes
		:type   body: AzureSecurityGroupRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-azure-securitygrouppolicy-viewmodels-azuresgpolicypostviewmodel
		:rtype  AzureSgPolicyPost

		"""
		route = f'{AzureSecurityGroupConsts.AZURE_SECURITY_GROUP_POLICY.value}/{azure_security_group_id}'
		return self._put(route=route, body=body)

	def delete(self, azure_security_group_id: str) -> None:
		"""Deletes Azure Security Group

		:link    https://api-v2-docs.dome9.com/index.html?python#azuresecuritygrouppolicy_delete
		:param   azure_security_group_id: Azure security group id.
		:type    azure_security_group_id: str
		:returns None

		"""
		route = f'{AzureSecurityGroupConsts.AZURE_SECURITY_GROUP_POLICY.value}/{azure_security_group_id}'
		return self._delete(route=route)

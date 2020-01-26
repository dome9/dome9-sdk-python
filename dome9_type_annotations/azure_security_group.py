from typing import Dict, List, Union

from resources.azure_security_group import AzureSecurityGroup as BaseAzureSecurityGroup, AzureSecurityGroupRequest


class azure_security_group(BaseAzureSecurityGroup):

	@classmethod
	def create(cls, body: AzureSecurityGroupRequest) -> Dict:
		"""Creates Azure Security Group

		:link   https://api-v2-docs.dome9.com/index.html?python#azuresecuritygrouppolicy_post
		:param  body: Azure Security Group request payload
		:type   body: AzureSecurityGroupRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-azure-securitygrouppolicy-viewmodels-azuresgpolicygetviewmodel
		:rtype  AzureSgPolicyGet

		"""
		pass

	@classmethod
	def get(cls, azure_security_group_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get Network Security Group Policies for the Azure accounts in the Dome9 account

		:link   https://api-v2-docs.dome9.com/index.html?python#azuresecuritygrouppolicy_get
		:param  azure_security_group_id: Dome9 azure security Group ID
		:param  azure_security_group_id: str
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-azure-securitygrouppolicy-viewmodels-azuresgpolicygetviewmodel
		:rtype  AzureSgPolicyGet

		"""
		pass

	@classmethod
	def update(cls, azure_security_group_id: str, body: AzureSecurityGroupRequest) -> Dict:
		"""Updates existing Azure Security Group

		:link   https://api-v2-docs.dome9.com/index.html?python#azuresecuritygrouppolicy_put
		:param  azure_security_group_id: Azure Security Group ID
		:param  azure_security_group_id: str
		:type   body: Details for the policy, including the changes
		:type   body: AzureSecurityGroupRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-azure-securitygrouppolicy-viewmodels-azuresgpolicypostviewmodel
		:rtype  AzureSgPolicyPost

		"""
		pass

	@classmethod
	def delete(cls, azure_security_group_id: str) -> None:
		"""Deletes Azure Security Group

		:link    https://api-v2-docs.dome9.com/index.html?python#azuresecuritygrouppolicy_delete
		:param   azure_security_group_id: Azure security group id.
		:type    azure_security_group_id: str
		:returns None

		"""
		pass

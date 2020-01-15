from typing import Dict, List

from resources.azure_security_group import AzureSecurityGroup as BaseAwsSecurityGroup, AzureSecurityGroupRequest


class azure_security_group(BaseAwsSecurityGroup):

	@classmethod
	def create(cls, body: AzureSecurityGroupRequest) -> Dict:
		pass

	@classmethod
	def get(cls, azure_security_group_id: str) -> Dict:
		pass

	@classmethod
	def get_all(cls) -> List[Dict]:
		pass

	@classmethod
	def update(cls, azure_security_group_id: str, body: AzureSecurityGroupRequest) -> Dict:
		pass

	@classmethod
	def delete(cls, azure_security_group_id: str) -> None:
		pass
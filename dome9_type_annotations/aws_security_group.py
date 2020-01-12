from typing import Dict, List

from resources.aws_security_group import AwsSecurityGroup as BaseAwsSecurityGroup, GetSecurityGroupParameters, AwsSecurityGroupRequest, UpdateSecurityGroupProtectionModeParameters, \
 BoundServices


class aws_security_group(BaseAwsSecurityGroup):

	@classmethod
	def create(cls, body: AwsSecurityGroupRequest) -> Dict:
		pass

	@classmethod
	def get(cls, security_group_id: str) -> Dict:
		pass

	@classmethod
	def get_all_in_region(cls, body: GetSecurityGroupParameters) -> List[Dict]:
		pass

	@classmethod
	def get_all(cls) -> List[Dict]:
		pass

	@classmethod
	def update(cls, security_group_id: str, body: AwsSecurityGroupRequest) -> Dict:
		pass

	@classmethod
	def update_protection_mode(cls, security_group_id: str, body: UpdateSecurityGroupProtectionModeParameters) -> Dict:
		pass

	@classmethod
	def handle_bound_services(cls, security_group_id: str, policy_type: str, body: BoundServices) -> Dict:
		pass

	@classmethod
	def delete(cls, security_group_id: str) -> None:
		pass

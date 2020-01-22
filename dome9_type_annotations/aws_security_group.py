from typing import Dict, List, Union

from resources.aws_security_group import AwsSecurityGroup as BaseAwsSecurityGroup, CloudSecurityGroup, CloudSecurityGroupProtectionModeChange, \
 CloudSecurityGroupService


class aws_security_group(BaseAwsSecurityGroup):

	@classmethod
	def create(cls, body: CloudSecurityGroup) -> Dict:
		"""Create aws security group

		:link https://api-v2-docs.dome9.com/#cloudsecuritygroup_createcloudsecuritygroup
		:param body: Details for the new aws security group
		:type body: CloudSecurityGroup
		:returns: Dict that has metadata for the created aws security group

		"""
		pass

	@classmethod
	def get(cls, security_group_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get aws security group

		:link   https://api-v2-docs.dome9.com/#cloudsecuritygroup_get
		:param  security_group_id: Dome9 aws security group id
		:type   security_group_id: str
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudsecuritygroupviewmodel
		:rtype  CloudSecurityGroup

		"""
		pass

	@classmethod
	def get_all_in_region(cls, cloud_account_id: str, region_id: str) -> List[Dict]:
		"""Get aws security groups for a specific cloud account and region

		:link   https://api-v2-docs.dome9.com/#cloudsecuritygroup_get
		:param  cloud_account_id: the cloud account id
		:type   cloud_account_id: str
		:param  region_id: the region
		:type   region_id: str
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudsecuritygroupviewmodel
		:rtype  List[CloudSecurityGroup]

		"""
		pass

	@classmethod
	def update(cls, security_group_id: str, body: CloudSecurityGroup) -> Dict:
		"""Updates an AWS security group protection mode

		:link  https://api-v2-docs.dome9.com/#cloudsecuritygroup_updatesecgroup
		:param security_group_id: the AWS security group id
		:type  security_group_id: str
		:param body: updated details for the security group. only 'IsProtected' is used in this call which defines whether to protect or unprotect the security group.
		:type  body: CloudSecurityGroup

		"""
		pass

	@classmethod
	def change_protection_mode(cls, security_group_id: str, body: CloudSecurityGroupProtectionModeChange) -> Dict:
		"""Change the protection mode for an AWS security group

		:link https://api-v2-docs.dome9.com/#cloudsecuritygroup_changeprotectionmode
		:param security_group_id: the AWS security group id (Dome9 internal ID / AWS security group ID)
		:type security_group_id: str
		:param body: details for the security group, including the protection mode. Only 'ProtectionMode' is required in this call (FullManage or ReadOnly).
		:type body: CloudSecurityGroupProtectionModeChange
		:return metadata
		:rtype Dict

		"""
		pass

	@classmethod
	def update_security_group_service(cls, security_group_id: str, policy_type: str, body: CloudSecurityGroupService) -> Dict:
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
		pass

	@classmethod
	def delete(cls, security_group_id: str) -> None:
		"""Delete aws security group

		:link https://api-v2-docs.dome9.com/#cloudsecuritygroup_deletecloudsecuritygroup
		:param security_group_id: Aws security group id.
		:type security_group_id: str
		:returns: None

		"""
		pass

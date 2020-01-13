from typing import Dict, List

from resources.aws_cloud_account import AwsCloudAccount as BaseAwsCloudAccount, AwsCloudAccountUpdateCredentials, AwsCloudAccountUpdateOrganizationalUnitID, \
	AwsCloudAccountUpdateConfig, AwsCloudAccountUpdateName, AwsCloudAccountRequest, AttachIamSafe, RestrictedIamEntitiesRequest


class aws_cloud_account(BaseAwsCloudAccount):

	@classmethod
	def create(cls, body: AwsCloudAccountRequest):
		pass

	@classmethod
	def get(cls, aws_cloud_account_id: str) ->Dict:
		pass

	@classmethod
	def get_all(cls) -> List[Dict]:
		pass

	@classmethod
	def update_name(cls, body: AwsCloudAccountUpdateName) -> Dict:
		pass

	@classmethod
	def update_region_config(cls, body: AwsCloudAccountUpdateConfig) -> Dict:
		pass

	@classmethod
	def update_organizational_id(cls, aws_cloud_account_id: str, body: AwsCloudAccountUpdateOrganizationalUnitID) -> Dict:
		pass

	@classmethod
	def update_credentials(cls, body: AwsCloudAccountUpdateCredentials) -> Dict:
		pass

	@classmethod
	def delete(cls, aws_cloud_account_id: str):
		pass

	@classmethod
	def attach_iam_safe(cls, body: AttachIamSafe) -> Dict:
		pass

	@classmethod
	def detach_iam_safe(cls, aws_cloud_account_id: str) -> None:
		pass

	@classmethod
	def protect_iam_safe_entity(cls, aws_cloud_account_id: str, body: RestrictedIamEntitiesRequest) -> str:
		pass

	@classmethod
	def get_all_protected_iam_safe_entity(cls, aws_cloud_account_id: str) -> Dict:
		pass

	@classmethod
	def unprotect_iam_safe_entity(cls, aws_cloud_account_id, entity_name: str, entity_type: str) -> None:
		pass

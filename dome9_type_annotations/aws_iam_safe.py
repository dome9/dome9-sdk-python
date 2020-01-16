from typing import Dict, List

from resources.aws_iam_safe import AwsIamSafe as BaseAwsSecurityGroup, RestrictedIamEntitiesRequest, AttachIamSafe


class aws_iam_safe(BaseAwsSecurityGroup):

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
	def unprotect_iam_safe_entity(cls, aws_cloud_account_id: str, entity_name: str, entity_type: str) -> None:
		pass

	@classmethod
	def protect_iam_safe_with_elevation(cls, aws_cloud_account_id: str, entity_name: str, entity_type: str, users_ids_to_protect: List[str]) -> None:
		pass

	@classmethod
	def update_iam_safe_with_elevation(cls, aws_cloud_account_id: str, entity_name: str, entity_type: str, users_ids_to_protect: List[str]) -> None:
		pass

	@classmethod
	def unprotect_iam_safe_with_elevation(cls, aws_cloud_account_id: str, entity_name: str, entity_type: str) -> None:
		pass

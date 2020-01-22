from typing import Dict, List

from resources.aws_iam_safe import AwsIamSafe as BaseAwsSecurityGroup, RestrictedIamEntitiesRequest, AttachIamSafe


class aws_iam_safe(BaseAwsSecurityGroup):

	@classmethod
	def attach_iam_safe(cls, body: AttachIamSafe) -> Dict:
		"""Attach iam safe to aws cloud account

		:link
		:param    body: Details for aws cloud account in order to attach to iam safe
		:type     body: AttachIamSafe
		:returns: Dict that has metadata for attached aws cloud account
		:rtype    Dict

		"""
		pass

	@classmethod
	def detach_iam_safe(cls, aws_cloud_account_id: str) -> None:
		"""Detach iam safe to aws cloud account

		:link
		:param    aws_cloud_account_id: Aws cloud account id
		:type     aws_cloud_account_id: str
		:returns: None

		"""
		pass

	@classmethod
	def protect_iam_safe_entity(cls, aws_cloud_account_id: str, body: RestrictedIamEntitiesRequest) -> str:
		"""Protect iam safe entity where the entity can be User or Role

		:param    aws_cloud_account_id: Aws security group id.
		:type     aws_cloud_account_id: str
		:param    body: Details restricted iam entities request
		:type     body: RestrictedIamEntitiesRequest
		:returns: Aws User or Role arn that protected
		:rtype    str

		"""
		pass

	@classmethod
	def get_all_protected_iam_safe_entity(cls, aws_cloud_account_id: str) -> Dict:
		"""Get data for all the users and roles

		:link
		:param    aws_cloud_account_id: Aws security group id.
		:type     aws_cloud_account_id: str
		:returns: Dict that has two key, roles and users

		"""
		pass

	@classmethod
	def unprotect_iam_safe_entity(cls, aws_cloud_account_id: str, entity_name: str, entity_type: str) -> None:
		"""Unprotect specific iam safe entity

		:link
		:param    aws_cloud_account_id: Aws security group id.
		:type     aws_cloud_account_id: str
		:param    entity_type: entity type, must be User or Role
		:type     entity_type: str
		:param    entity_name: Entity name
		:type     entity_name: str
		:returns: None

		"""
		pass

	@classmethod
	def protect_iam_safe_with_elevation(cls, aws_cloud_account_id: str, entity_name: str, entity_type: str, users_ids_to_protect: List[str]) -> None:
		"""Protect iam safe with elevation

		:link
		:param   aws_cloud_account_id: Aws security group id.
		:type    aws_cloud_account_id: str
		:param   entity_name: Aws iam user name or aws role
		:type    entity_name: str
		:param   entity_type: Entity type, must be one of the following Role or User
		:type    entity_type: str
		:param   users_ids_to_protect: List of users ids to protect
		:type    users_ids_to_protect: List[str]
		:return: None

		"""
		pass

	@classmethod
	def update_iam_safe_with_elevation(cls, aws_cloud_account_id: str, entity_name: str, entity_type: str, users_ids_to_protect: List[str]) -> None:
		"""Protect iam safe with elevation

		:link
		:param   aws_cloud_account_id: Aws security group id.
		:type    aws_cloud_account_id: str
		:param   entity_name: Aws iam user name or aws role
		:type    entity_name: str
		:param   entity_type: Entity type, must be one of the following Role or User
		:type    entity_type: str
		:param   users_ids_to_protect: List of users ids to protect
		:type    users_ids_to_protect: List[str]
		:return: None

		"""
		pass

	@classmethod
	def unprotect_iam_safe_with_elevation(cls, aws_cloud_account_id: str, entity_name: str, entity_type: str) -> None:
		"""Protect iam safe with elevation

		:link
		:param   aws_cloud_account_id: Aws security group id.
		:type    aws_cloud_account_id: str
		:param   entity_name: Aws iam user name or aws role
		:type    entity_name: str
		:param   entity_type: Entity type, must be one of the following Role or User
		:type    entity_type: str
		:return: None

		"""
		pass

from resources.aws_cloud_account import AwsCloudAccount as BaseAwsCloudAccount, AwsCloudAccountUpdateCredentials, AwsCloudAccountUpdateOrganizationalUnitID, \
 AwsCloudAccountUpdateConfig, AwsCloudAccountUpdateName, AwsCloudAccountRequest, AttachIamSafe


class aws_cloud_account(BaseAwsCloudAccount):

	@classmethod
	def create(cls, body: AwsCloudAccountRequest):
		pass

	@classmethod
	def get(cls, aws_cloud_account_id: str):
		pass

	@classmethod
	def get_all(cls):
		pass

	@classmethod
	def update_name(cls, body: AwsCloudAccountUpdateName):
		pass

	@classmethod
	def update_region_config(cls, body: AwsCloudAccountUpdateConfig):
		pass

	@classmethod
	def update_organizational_id(cls, aws_cloud_account_id: str, body: AwsCloudAccountUpdateOrganizationalUnitID):
		pass

	@classmethod
	def update_credentials(cls, body: AwsCloudAccountUpdateCredentials):
		pass

	@classmethod
	def delete(cls, aws_cloud_account_id: str):
		pass

	@classmethod
	def attach_iam_safe_to_aws_cloud_account(cls, body: AttachIamSafe):
		pass

	@classmethod
	def detach_iam_safe_to_aws_cloud_account(cls, aws_cloud_account_id: str):
		pass

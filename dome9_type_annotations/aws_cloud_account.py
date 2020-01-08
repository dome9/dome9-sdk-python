from resources.aws_cloud_account import AwsCloudAccount as BaseAwsCloudAccount, AwsCloudAccountUpdateCredentials, AwsCloudAccountUpdateOrganizationalUnitID, \
 AwsCloudAccountUpdateConfig, AwsCloudAccountUpdateName, AwsCloudAccountRequest


class aws_cloud_account(BaseAwsCloudAccount):

	@classmethod
	def create(cls, body: AwsCloudAccountRequest):
		pass

	@classmethod
	def get(cls, awsCloudAccountID: str):
		pass

	@classmethod
	def getAll(cls):
		pass

	@classmethod
	def updateName(cls, body: AwsCloudAccountUpdateName):
		pass

	@classmethod
	def updateRegionConfig(cls, body: AwsCloudAccountUpdateConfig):
		pass

	@classmethod
	def updateOrganizationalID(cls, awsCloudAccountID: str, body: AwsCloudAccountUpdateOrganizationalUnitID):
		pass

	@classmethod
	def updateCredentials(cls, body: AwsCloudAccountUpdateCredentials):
		pass

	@classmethod
	def delete(cls, awsCloudAccountID: str):
		pass

	@classmethod
	def attachIAMSafeToAWSCloudAccount(cls, body: AttachIamSafe):
		pass

	@classmethod
	def detachIAMSafeToAWSCloudAccount(cls, awsCloudAccountID: str):
		pass

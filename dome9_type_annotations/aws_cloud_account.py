from resources.aws_cloud_account import AwsCloudAccount as BaseAwsCloudAccount


class aws_cloud_account(BaseAwsCloudAccount):

	@classmethod
	def create(cls, body):
		pass

	@classmethod
	def get(cls, awsCloudAccountID):
		pass

	@classmethod
	def getAll(cls):
		pass

	@classmethod
	def updateName(cls, body):
		pass

	@classmethod
	def updateRegionConfig(cls, body):
		pass

	@classmethod
	def updateOrganizationalID(cls, awsCloudAccountID, body):
		pass

	@classmethod
	def updateCredentials(cls, body):
		pass

	@classmethod
	def delete(cls, awsCloudAccountID):
		pass

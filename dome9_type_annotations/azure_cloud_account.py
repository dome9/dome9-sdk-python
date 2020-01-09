from resources.azure_cloud_account import AzureCloudAccount as BaseAzureCloudAccount, AzureCloudAccountUpdateOrganizationalUnitID, AzureCloudAccountUpdateCredentials, \
	AzureCloudAccountUpdateOperationMode, AzureCloudAccountUpdateName, AzureCloudAccountRequest


class azure_cloud_account(BaseAzureCloudAccount):

	@classmethod
	def create(cls, body: AzureCloudAccountRequest):
		pass

	@classmethod
	def get(cls, azure_cloud_account_id: str):
		pass

	@classmethod
	def get_all(cls):
		pass

	@classmethod
	def update_name(cls, azure_cloud_account_id: str, body: AzureCloudAccountUpdateName):
		pass

	@classmethod
	def update_operation_mode(cls, azure_cloud_account_id: str, body: AzureCloudAccountUpdateOperationMode):
		pass

	@classmethod
	def update_credentials(cls, azure_cloud_account_id: str, body: AzureCloudAccountUpdateCredentials):
		pass

	@classmethod
	def update_organizational_id(cls, azure_cloud_account_id: str, body: AzureCloudAccountUpdateOrganizationalUnitID):
		pass

	@classmethod
	def delete(cls, azure_cloud_account_id: str):
		pass


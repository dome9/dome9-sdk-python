from resources.azure_cloud_account import AzureCloudAccount as BaseAzureCloudAccount, AzureCloudAccountUpdateOrganizationalUnitID, AzureCloudAccountCredentialsPut, \
 AzureAccountOperationMode, AzureAccountNameMode, AzureCloudAccountRequest


class azure_cloud_account(BaseAzureCloudAccount):

	@classmethod
	def create(cls, body: AzureCloudAccountRequest):
		"""Add (onboard) an Azure account to the user's Dome9 account

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_post
		:param   body: details for the Azure account
		:type    body: AzureCloudAccountRequest
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		pass

	@classmethod
	def get(cls, azure_cloud_account_id: str = ''):
		"""Get details for all Azure accounts for the Dome9 user

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_get
		:param   azure_cloud_account_id:
		:type    azure_cloud_account_id: str
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		pass

	@classmethod
	def update_account_name(cls, azure_cloud_account_id: str, body: AzureAccountNameMode):
		"""Update the account name (in Dome9) for an Azure account

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_updateaccountname
		:param   azure_cloud_account_id: the account id in Dome9
		:type    azure_cloud_account_id: str
		:param   body: the new name for the account
		:type    body: AzureAccountNameMode
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		pass

	@classmethod
	def update_operation_mode(cls, azure_cloud_account_id: str, body: AzureAccountOperationMode):
		"""Update the operations mode for an Azure account in Dome9. Modes can be Read-Only or Manage

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_updateoperationmodeasync
		:param   azure_cloud_account_id: the account id for the Azure account in Dome9
		:type    azure_cloud_account_id: str
		:param   body: updated details for the account, including the operations mode
		:type    body: AzureAccountOperationMode
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		pass

	@classmethod
	def update_cloud_account_credentials(cls, azure_cloud_account_id: str, body: AzureCloudAccountCredentialsPut):
		"""

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_updatecloudaccountcredentials
		:param   azure_cloud_account_id:
		:type    azure_cloud_account_id: str
		:param   body:
		:type    body: AzureCloudAccountCredentialsPut
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		pass

	@classmethod
	def update_organizational_id(cls, azure_cloud_account_id: str, body: AzureCloudAccountUpdateOrganizationalUnitID):
		"""Update the ID of the Organizational Unit that this cloud account will be attached to. Use 'null' for th root organizational unit

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_updateorganziationalid
		:param   azure_cloud_account_id: The Dome9 Guid ID of the Azure cloud account
		:type    azure_cloud_account_id: str
		:param   body: The Guid ID of the Organizational Unit to attach to. Use 'null' to attach to the root Organizational Unit
		:type    body: AzureCloudAccountUpdateOrganizationalUnitID
		:return: https://api-v2-docs.dome9.com/#schemadome9-web-api-models-azurecloudaccountviewmodel
		:rtype   AzureCloudAccountRequest

		"""
		pass

	@classmethod
	def delete(cls, azure_cloud_account_id: str):
		"""Delete an Azure account from a Dome9 account (the Azure account is not deleted from Azure)

		:link    https://api-v2-docs.dome9.com/#azurecloudaccount_delete
		:param   azure_cloud_account_id: the Dome9 account id for the account
		:type    azure_cloud_account_id: str
		:return: None

		"""
		pass

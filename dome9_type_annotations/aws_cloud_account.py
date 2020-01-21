from typing import Dict, List, Union

from resources.aws_cloud_account import AwsCloudAccount as BaseAwsCloudAccount, CloudAccountCredentialsViewModel, CloudAccountUpdateOrganizationalUnitId, \
 CloudAccountRegionConfigurationViewModel, AwsCloudAccountUpdateName, CloudAccount


class aws_cloud_account(BaseAwsCloudAccount):

	@classmethod
	def create(cls, body: CloudAccount):
		"""Create (onboard) aws cloud account

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_post
		:param   body: Details for the new aws cloud account
		:type    body: CloudAccount
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype   CloudAccount

		"""
		pass

	@classmethod
	def get(cls, aws_cloud_account_id: str = '') -> Union[Dict, List[Dict]]:
		"""Fetch a specific AWS cloud account

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_get
		:param   aws_cloud_account_id: Dome9 aws cloud account id
		:type    aws_cloud_account_id: str
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype    CloudAccount

		"""
		pass

	@classmethod
	def update_cloud_account_name(cls, body: AwsCloudAccountUpdateName) -> Dict:
		"""Update an AWS cloud account name

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_updatecloudaccountname
		:param   body: Details for dome9 aws cloud account
		:type    body: AwsCloudAccountUpdateName
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype   CloudAccount

		"""
		pass

	@classmethod
	def update_region_config(cls, body: CloudAccountRegionConfigurationViewModel) -> Dict:
		"""Update an AWS cloud account region configuration

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_updatecloudaccountregionconf
		:param   body: updated Regional Configuration parameters for the account
		:type    body: CloudAccountRegionConfigurationViewModel
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype   CloudAccount

		"""
		pass

	@classmethod
	def update_organizational_id(cls, aws_cloud_account_id: str, body: CloudAccountUpdateOrganizationalUnitId) -> Dict:
		"""Update the ID of the Organizational Unit that this cloud account will be attached to. Use 'null' for the root Organizational Unit

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_updateorganziationalid
		:param   aws_cloud_account_id: The Dome9 Guid ID of the AWS cloud account
		:type    aws_cloud_account_id: str
		:param   body: The Guid ID of the Organizational Unit to attach to. Use 'null' to attach to the root Organizational Unit
		:type    body: CloudAccountUpdateOrganizationalUnitId
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype   CloudAccount

		"""
		pass

	@classmethod
	def update_credentials(cls, body: CloudAccountCredentialsViewModel) -> Dict:
		"""Update credentials for an AWS cloud account in Dome9. At least one of the following properties must be provided: "cloudAccountId", "externalAccountNumber"

		:link    https://api-v2-docs.dome9.com/#cloudaccounts_updatecloudaccountcredentials
		:param   body: credentials block
		:type    body: CloudAccountCredentialsViewModel
		:returns https://api-v2-docs.dome9.com/#schemadome9-web-api-models-cloudaccountviewmodel
		:rtype   CloudAccount

		"""
		pass

	@classmethod
	def delete(cls, aws_cloud_account_id: str):
		"""Delete an AWS cloud account

		:link https://api-v2-docs.dome9.com/#cloudaccounts_delete
		:param aws_cloud_account_id: The Dome9 AWS account id (UUID)
		:type aws_cloud_account_id: str
		:returns: None

		"""
		pass

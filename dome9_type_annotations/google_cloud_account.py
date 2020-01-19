from typing import Dict, List, Union

from resources.google_cloud_account import GoogleCloudAccount as BaseGoogleCloudAccount, GoogleCloudAccountUpdate, GoogleAccountGsuite, GoogleAccountName, GoogleCloudAccountPost


class google_cloud_account(BaseGoogleCloudAccount):

	@classmethod
	def create(cls, body: GoogleCloudAccountPost) -> Dict:
		"""Add (onboard) a new Google cloud account to Dome9

		:link    https://api-v2-docs.dome9.com/index.html#googlecloudaccount_post
		:param   body: details for the new account
		:type    body: GoogleCloudAccountRequest
		:return  https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googlecloudaccountgetviewmodel
		:rtype   GoogleAccountGsuite

		"""
		pass

	@classmethod
	def get(cls, google_cloud_account_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get details for a specific Google Cloud Account

		:link    https://api-v2-docs.dome9.com/index.html#googlecloudaccount_get
		:param   google_cloud_account_id: the Google cloud account id , if id is not provided will return all google accounts
		:type    google_cloud_account_id: str
		:return  https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googlecloudaccountgetviewmodel
		:rtype   GoogleCloudAccountGet

		"""
		pass

	@classmethod
	def update_account_name(cls, gcp_cloud_account_id: str, body: GoogleAccountName) -> Dict:
		"""Update a Google Cloud account name (as it appears in Dome9)

		:link:  https://api-v2-docs.dome9.com/index.html#googlecloudaccount_updateaccountname
		:param  gcp_cloud_account_id: the account id
		:type   gcp_cloud_account_id: str
		:param  body: the updated name as it will appear in Dome9
		:type   body: AwsCloudAccountUpdateName
		:return https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googleaccountnameviewmodel
		:rtype  GoogleCloudAccountGet

		"""
		pass

	@classmethod
	def delete(cls, google_cloud_account_id: str) -> None:
		"""Delete a Google cloud account (from Dome9)

		:link: https://api-v2-docs.dome9.com/index.html#googlecloudaccount_delete
		:param google_cloud_account_id: The Id of the Google cloud account
		:type  google_cloud_account_id: str
		:return: None

		"""
		pass

	@classmethod
	def update_account_gsuite(cls, google_cloud_account_id: str, body: GoogleAccountGsuite) -> Dict:
		"""Update a Google Cloud account Gsuite data

		:link https://api-v2-docs.dome9.com/index.html#googlecloudaccount_updateaccountgsuite
		:param  google_cloud_account_id: The Id of the Google cloud account
		:type   google_cloud_account_id: str
		:param  body: the updated Gsuite as it will uses in Dome9
		:type   body: GoogleAccountGsuite
		:return https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googlecloudaccountgetviewmodel
		:rtype  GoogleCloudAccountGet

		"""
		pass

	@classmethod
	def update_google_cloud_account_credentials(cls,
		google_cloud_account_id: str,
		body: GoogleCloudAccountUpdate,
		skip_compute_validation: bool = False) -> Dict:
		"""Update Google Cloud Account Credentials

		:link https://api-v2-docs.dome9.com/index.html#googlecloudaccount_updategooglecloudaccountcredentials
		:param  google_cloud_account_id: The Id of the Google cloud account
		:type   google_cloud_account_id: str
		:param  body: google cloudAccount update object
		:type   body: GoogleCloudAccountUpdate
		:param  skip_compute_validation: if true will skip compute validation
		:type   skip_compute_validation: bool
		:return https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-google-accounts-googlecloudaccountupdateviewmodel
		:rtype  GoogleCloudAccountGet

		"""
		pass

	@classmethod
	def move_cloud_accounts_to_organizational_unit(cls, body) -> Dict:
		"""Detach cloud accounts from an Organizational unit and attach them to another Organizational unit Use 'null' for root organizational unit

		:link    https://api-v2-docs.dome9.com/index.html#googlecloudaccount_movecloudaccountstoorganizationalunit
		:param   body:
		:type    body: MoveOrganizationalUnit
		:return: None

		"""
		pass

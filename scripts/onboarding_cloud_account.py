#!/usr/bin/env python
import argparse
import uuid
from typing import Dict

from loguru import logger

from dome9_type_annotations.client import Client
from resources.aws_cloud_account import CloudAccount, CloudAccountCredentials, CloudAccountUpdateOrganizationalUnitId
from resources.azure_cloud_account import AzureCloudAccountRequest, AzureAccountCredentials, AzureCloudAccountUpdateOrganizationalUnitID
from resources.role import UpdateRole, Permissions


class OnBoardingCloudAccount:

	VENDOR_TYPES = ['aws', 'azure']
	AWS_ALLOW_READONLY = [True, False]
	AWS_FULL_PROTECTION = [True, False]
	AWS_SRL = '1'
	AZURE_OPERATION_MODE = ['Read', 'Manage']
	AZURE_SRL = '7'

	def __init__(self, args: argparse.Namespace):
		self.args: Dict = vars(args)
		self.d9_client = Client(access_id=args.dome9ApiKeyID, secret_key=args.dome9ApiKeySecret)

	def onboarding_new_account(self) -> str:
		if self.args['cloudVendorType'] == 'aws':
			credentials = CloudAccountCredentials(arn=self.args['awsRoleArn'], secret=self.args['awsRoleExternalID'])
			payload = CloudAccount(name=self.args['dome9CloudAccountName'], credentials=credentials)
			resp = self.d9_client.aws_cloud_account.create(body=payload)

			return resp['id']

		else:
			credentials = AzureAccountCredentials(client_id=self.args['azureApplicationID'], client_password=self.args['azureSecretKey'])
			payload = AzureCloudAccountRequest(name=self.args['dome9CloudAccountName'],
				subscription_id=self.args['azureSubscriptionID'],
				tenant_id=self.args['azureActiveDirectoryID'],
				credentials=credentials,
				operation_mode=self.args['azureOperationMode'])
			resp = self.d9_client.azure_cloud_account.create(body=payload)

			return resp['id']

	def attach_oi_to_cloud_account(self, cloud_account_id: str) -> None:
		if self.args['cloudVendorType'] == 'aws':
			payload = CloudAccountUpdateOrganizationalUnitId(organizational_unit_id=self.args['dome9OuID'])
			self.d9_client.aws_cloud_account.update_organizational_id(aws_cloud_account_id=cloud_account_id, body=payload)

		else:
			payload = AzureCloudAccountUpdateOrganizationalUnitID(organizational_unit_id=self.args['dome9OuID'])
			self.d9_client.azure_cloud_account.update_organizational_id(azure_cloud_account_id=cloud_account_id, body=payload)

	def main_process(self) -> None:
		logger.info(f'''onboarding {self.args['cloudVendorType']} account''')
		cloud_account_id = self.onboarding_new_account()

		if self.args['dome9OuID']:
			logger.info(f'''attach cloud_account {cloud_account_id} to OU {self.args['dome9OuID']}''')
			self.attach_oi_to_cloud_account(cloud_account_id=cloud_account_id)

		if self.args['cloudVendorType'] == 'aws':
			srl = '|'.join([OnBoardingCloudAccount.AWS_SRL, cloud_account_id])
		else:
			srl = '|'.join([OnBoardingCloudAccount.AZURE_SRL, cloud_account_id])

		if self.args['dome9AdminRoleID']:
			logger.info(f'''grant admin permission to role {self.args['dome9AdminRoleID']}''')
			role_object = self.d9_client.role.get(role_id=self.args['dome9AdminRoleID'])
			permission = role_object['permissions']
			manage_permission = permission['manage']
			access_permission = permission['access']
			create_permission = permission['create']
			view_permission = permission['view']
			manage_permission.append(srl)
			create_permission.append(srl)
			access_permission.append(srl)
			view_permission.append(srl)
			permissions = Permissions(manage=manage_permission, create=create_permission, access=access_permission, view=view_permission)
			payload = UpdateRole(name=role_object['name'], description='dome9 admin role', permissions=permissions)
			self.d9_client.role.update(role_id=self.args['dome9AdminRoleID'], body=payload)

		if self.args['dome9ViewRoleID']:
			logger.info(f'''grant view permission to role {self.args['dome9ViewRoleID']}''')
			role_object = self.d9_client.role.get(self.args['dome9ViewRoleID'])
			permission = role_object['permissions']
			view_permission = permission['view']
			view_permission.append(srl)
			permissions = Permissions(view=view_permission)
			payload = UpdateRole(name=role_object['name'], description='dome9 view role', permissions=permissions)
			self.d9_client.role.update(role_id=self.args['dome9AdminRoleID'], body=payload)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='cloud account onboarding parameters')
	useExample = '''
	AWS:
	--dome9ApiKeyID sdfsdfssdf --dome9ApiKeySecret sdfsdfssdf --cloudVendorType aws --awsRoleArn arn:aws:iam::111111111:role/Dome9-Connect --awsRoleExternalID sdfsdfsdff --dome9OuID e21b3e8b-e02f-46df-bd70-8ce65ca8a3a5 --dome9CloudAccountName production --dome9AdminRoleID 118187 --dome9ViewRoleID 118203

	Azure:
	--dome9ApiKeyID ddsfsdfsdf --dome9ApiKeySecret sdfsdfssdf --cloudVendorType azure --azureSubscriptionID sdfsdfsdfsdfsd --azureActiveDirectoryID sdfsdsdfsdsdfsd --azureApplicationID sfsdfsdfsfdsdf --azureSecretKey sdfsfsfsfd --dome9OuID 92f9a334-bf29-48a5-9cf8-66a10efe51e6 --dome9CloudAccountName production --dome9AdminRoleID 118881 --dome9ViewRoleID 118901 --azureOperationMode Manage
	'''
	parser.epilog = f'Example of use: {__file__} {useExample}'
	parser.add_argument('--dome9ApiKeyID', required=True, type=str, help='dome9 api key')
	parser.add_argument('--dome9ApiKeySecret', required=True, type=str, help='dome9 secret key')
	parser.add_argument('--cloudVendorType',
		required=True,
		type=str,
		choices=OnBoardingCloudAccount.VENDOR_TYPES,
		help='type of cloud account vendor: aws, azure')
	parser.add_argument('--awsRoleArn', required=True, type=str, help='the arn of the dome9-connect role in your aws account')
	parser.add_argument('--awsRoleExternalID',
		required=True,
		type=str,
		help='the external id value used to create the role in your aws account')
	parser.add_argument('--awsAllowReadOnly',
		action='store_true',
		help='switch parameter, use it for read-only, don\'t use it for full protection')
	parser.add_argument(
		'--awsFullProtection',
		action='store_true',
		help=
		'switch parameter, use it for to set the security groups in the account to full-protection in the course of onboarding, or don\'t use it to leave them unchanged'
	)
	parser.add_argument('--azureSubscriptionID', type=str, help='azure subscriptionid')
	parser.add_argument('--azureActiveDirectoryID', type=str, help='azure azureactivedirectoryid\\tenantid')
	parser.add_argument('--azureApplicationID', type=str, help='azure azureapplicationid\clientid')
	parser.add_argument('--azureSecretKey', type=str, help='azure azuresecretkey\clientpassword')
	parser.add_argument('--azureOperationMode',
		type=str,
		default='Read',
		choices=OnBoardingCloudAccount.AZURE_OPERATION_MODE,
		help='default=read, azure operationmode, allow read or manage')
	parser.add_argument('--dome9CloudAccountName',
		type=str,
		default='account-{}'.format(str(uuid.uuid4())[:8]),
		help='default=account-randomstring , accountname display on dome9 console')
	parser.add_argument('--dome9OuID', type=str, help='organization unit id to attach cloud account')
	parser.add_argument('--dome9AdminRoleID', type=str, help='dome9 role id to get admin permission to the account')
	parser.add_argument('--dome9ViewRoleID', type=str, help='dome9 role id to get read permission to the account')

	arguments = parser.parse_args()
	TestD9Api = OnBoardingCloudAccount(arguments)
	TestD9Api.main_process()

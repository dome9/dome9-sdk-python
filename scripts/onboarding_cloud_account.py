#!/usr/bin/env python
import argparse
import uuid
import sys

from dome9_type_annotations.client import Client
from resources.aws_cloud_account import CloudAccount, CloudAccountCredentials, CloudAccountUpdateOrganizationalUnitId
from resources.azure_cloud_account import AzureCloudAccountRequest, AzureAccountCredentials, AzureCloudAccountUpdateOrganizationalUnitID
from resources.role import UpdateRole, Permissions


class OnBoardingCloudAccount(object):

	VENDOR_TYPES = ['aws', 'azure']
	AWS_ALLOW_READONLY = [True, False]
	AWS_FULL_PROTECTION = [True, False]
	AWS_SRL = '1'
	AZURE_OPERATION_MODE = ['Read', 'Manage']
	AZURE_SRL = '7'

	def __init__(self, args):
		self.args = args
		self.d9_client = Client(access_id=args.dome9ApiKeyID, secret_key=args.dome9ApiKeySecret)

	def onboarding_new_account(self):
		if self.args.cloudVendorType == 'aws':
			credentials = CloudAccountCredentials(arn=self.args.awsRoleArn, secret=self.args.awsRoleExternalID)
			payload = CloudAccount(name=self.args.dome9CloudAccountName, credentials=credentials)
			resp = self.d9_client.aws_cloud_account.create(body=payload)
			return resp['id']

		elif self.args.cloudVendorType == 'azure':
			credentials = AzureAccountCredentials(client_id=self.args.azureApplicationID, client_password=self.args.azureSecretKey)
			payload = AzureCloudAccountRequest(name=self.args.dome9CloudAccountName,
				subscription_id=self.args.azureSubscriptionID,
				tenant_id=self.args.azureActiveDirectoryID,
				credentials=credentials,
				operation_mode=self.args.azureOperationMode)
			resp = self.d9_client.azure_cloud_account.create(body=payload)
			return resp['id']

	def attach_oi_to_cloud_account(self, cloud_account_id):
		if self.args.cloudVendorType == 'aws':
			payload = CloudAccountUpdateOrganizationalUnitId(organizational_unit_id=self.args.dome9OuID)
			self.d9_client.aws_cloud_account.update_organizational_id(aws_cloud_account_id=cloud_account_id, body=payload)

		elif self.args.cloudVendorType == 'azure':
			payload = AzureCloudAccountUpdateOrganizationalUnitID(organizational_unit_id=self.args.dome9OuID)
			self.d9_client.azure_cloud_account.update_organizational_id(azure_cloud_account_id=cloud_account_id, body=payload)

	def main_process(self):
		print(f'onboarding {self.args.cloudVendorType} account')
		cloud_account_id = self.onboarding_new_account()

		if self.args.dome9OuID:
			print(f'attach cloud_account {cloud_account_id} to OU {self.args.dome9OuID}')
			self.attach_oi_to_cloud_account(cloud_account_id=cloud_account_id)

		if self.args.cloudVendorType == 'aws':
			srl = '|'.join([OnBoardingCloudAccount.AWS_SRL, cloud_account_id])
		elif self.args.cloudVendorType == 'azure':
			srl = '|'.join([OnBoardingCloudAccount.AZURE_SRL, cloud_account_id])

		if self.args.dome9AdminRoleID:
			print(f'grant admin permission to role {self.args.dome9AdminRoleID}')
			role_object = self.d9_client.role.get(role_id=self.args.dome9AdminRoleID)
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
			self.d9_client.role.update(role_id=self.args.dome9AdminRoleID, body=payload)

		if self.args.dome9ViewRoleID:
			print(f'grant view permission to role {self.args.dome9ViewRoleID}')
			role_object = self.d9_client.role.get(self.args.dome9ViewRoleID)
			permission = role_object['permissions']
			view_permission = permission['view']
			view_permission.append(srl)
			permissions = Permissions(view=view_permission)
			payload = UpdateRole(name=role_object['name'], description='dome9 view role', permissions=permissions)
			self.d9_client.role.update(role_id=self.args.dome9AdminRoleID, body=payload)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='')
	useExample = '''
	AWS:
	--dome9ApiKeyID sdfsdfssdf --dome9ApiKeySecret sdfsdfssdf --cloudVendorType aws --awsRoleArn arn:aws:iam::111111111:role/Dome9-Connect --awsRoleExternalID sdfsdfsdff --dome9OuID e21b3e8b-e02f-46df-bd70-8ce65ca8a3a5 --dome9CloudAccountName production --dome9AdminRoleID 118187 --dome9ViewRoleID 118203

	Azure:
	--dome9ApiKeyID ddsfsdfsdf --dome9ApiKeySecret sdfsdfssdf --cloudVendorType azure --azureSubscriptionID sdfsdfsdfsdfsd --azureActiveDirectoryID sdfsdsdfsdsdfsd --azureApplicationID sfsdfsdfsfdsdf --azureSecretKey sdfsfsfsfd --dome9OuID 92f9a334-bf29-48a5-9cf8-66a10efe51e6 --dome9CloudAccountName production --dome9AdminRoleID 118881 --dome9ViewRoleID 118901 --azureOperationMode Manage
	'''
	parser.epilog = 'Example of use: {} {}'.format(__file__, useExample)
	parser.add_argument('--dome9ApiKeyID', required=True, type=str, help='(required) Dome9 Api key')
	parser.add_argument('--dome9ApiKeySecret', required=True, type=str, help='(required) Dome9 secret key')
	parser.add_argument('--cloudVendorType',
		required=True,
		type=str,
		choices=OnBoardingCloudAccount.VENDOR_TYPES,
		help='(required) type of cloud account vendor: aws, azure')
	parser.add_argument('--awsRoleArn', required=True, type=str, help='(required) The ARN of the Dome9-Connect role in your AWS account')
	parser.add_argument('--awsRoleExternalID',
		required=True,
		type=str,
		help='(required) The external ID value used to create the role in your AWS account')
	parser.add_argument('--awsAllowReadOnly',
		required=False,
		action='store_true',
		help='switch parameter, use it for Read-Only, don\'t use it for Full Protection')
	parser.add_argument(
		'--awsFullProtection',
		required=False,
		action='store_true',
		help=
		'switch parameter, use it for to set the Security Groups in the account to Full-Protection in the course of onboarding, or don\'t use it to leave them unchanged'
	)
	parser.add_argument('--azureSubscriptionID', required=False, type=str, help='Azure subscriptionID')
	parser.add_argument('--azureActiveDirectoryID', required=False, type=str, help='Azure azureActiveDirectoryID\\tenantID')
	parser.add_argument('--azureApplicationID', required=False, type=str, help='Azure azureApplicationID\clientID')
	parser.add_argument('--azureSecretKey', required=False, type=str, help='Azure azureSecretKey\clientPassword')
	parser.add_argument('--azureOperationMode',
		required=False,
		type=str,
		default='Read',
		choices=OnBoardingCloudAccount.AZURE_OPERATION_MODE,
		help='Default=Read, Azure operationMode, allow Read or Manage')
	parser.add_argument('--dome9CloudAccountName',
		required=False,
		type=str,
		default='account-{}'.format(str(uuid.uuid4())[:8]),
		help='Default=account-randomString , accountName display on Dome9 console')
	parser.add_argument('--dome9OuID', required=False, type=str, help='Organization Unit ID to attach cloud account')
	parser.add_argument('--dome9AdminRoleID', required=False, type=str, help='Dome9 role ID to get admin permission to the account')
	parser.add_argument('--dome9ViewRoleID', required=False, type=str, help='Dome9 role ID to get read permission to the account')

	arguments = parser.parse_args()
	TestD9Api = OnBoardingCloudAccount(arguments)
	TestD9Api.main_process()

from dome9.client import Client as BaseClient
from dome9_type_annotations.aws_cloud_account import aws_cloud_account
from dome9_type_annotations.azure_cloud_account import azure_cloud_account


class Client(BaseClient):

	aws_cloud_account: 'aws_cloud_account'
	azure_cloud_account: 'azure_cloud_account'

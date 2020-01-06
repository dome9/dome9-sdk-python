from dome9.client import Client as BaseClient
from dome9_type_annotations.aws_cloud_accounts import aws_cloud_accounts


class Client(BaseClient):

	aws_cloud_accounts: 'aws_cloud_accounts'

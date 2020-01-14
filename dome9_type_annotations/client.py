from dome9.client import Client as BaseClient
from dome9_type_annotations.aws_cloud_account import aws_cloud_account
from dome9_type_annotations.azure_cloud_account import azure_cloud_account
from dome9_type_annotations.aws_security_group import aws_security_group
from dome9_type_annotations.rule_bundle import rule_bundle


class Client(BaseClient):

	aws_cloud_account: 'aws_cloud_account'
	azure_cloud_account: 'azure_cloud_account'
	aws_security_group: 'aws_security_group'
	rule_bundle: 'rule_bundle'

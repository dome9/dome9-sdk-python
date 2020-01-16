from dome9.client import Client as BaseClient
from dome9_type_annotations.aws_cloud_account import aws_cloud_account
from dome9_type_annotations.azure_cloud_account import azure_cloud_account
from dome9_type_annotations.aws_security_group import aws_security_group
from dome9_type_annotations.organizational_unit import organizational_unit
from dome9_type_annotations.azure_security_group import azure_security_group
from dome9_type_annotations.rule_bundle import rule_bundle
from dome9_type_annotations.continuous_compliance_policy import continuous_compliance_policy
from dome9_type_annotations.aws_iam_safe import aws_iam_safe
from dome9_type_annotations.access_lease import access_lease
from dome9_type_annotations.user import user


class Client(BaseClient):

	aws_cloud_account: 'aws_cloud_account'
	azure_cloud_account: 'azure_cloud_account'
	aws_security_group: 'aws_security_group'
	organizational_unit: 'organizational_unit'
	azure_security_group: 'azure_security_group'
	rule_bundle: 'rule_bundle'
	continuous_compliance_notification: 'continuous_compliance_notification'
	continuous_compliance_policy: 'continuous_compliance_policy'
	aws_iam_safe: 'aws_iam_safe'
	access_lease: 'access_lease'
	user: 'user'

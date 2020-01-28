from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union

from dome9 import APIUtils
from dome9.client import Client
from dome9.base_dataclass import BaseDataclassRequest
from dome9.exceptions import UnsupportedScheduleDataReportType, UnsupportedNotificationOutputFormat, UnsupportedNotificationSystemType

from dome9.resource import Dome9Resource


class ScheduleDataReportType(Enum):
	DETAILED = 'Detailed'
	SUMMARY = 'Summary'
	FULL_CSV = 'FullCsv'
	FULL_CSV_ZIP = 'FullCsvZip'


class SystemType(Enum):
	SERVICE_NOW = 'ServiceNow'
	JIRA = 'Jira'
	PAGER_DUTY = 'PagerDuty'


class HttpMethod(Enum):
	POST = 'Post'
	PUT = 'Put'


class AuthMethod(Enum):
	NO_AUTH = 'NoAuth'
	BASIC_AUTH = 'BasicAuth'


class WebhookNotificationDataFormatType(Enum):
	JSON_WITH_FULL_ENTITY = 'JsonWithFullEntity'
	JSON_WITH_BASIC_ENTITY = 'JsonWithBasicEntity'
	JSON = 'Json'
	PLAIN_TEXT = 'PlainText'
	SPLUNK_BASIC = 'SplunkBasic'
	SERVICE_NOW = 'ServiceNow'


class ContinuousComplianceNotificationConsts(Enum):
	CONTINUOUS_COMPLIANCE_NOTIFICATION = 'Compliance/ContinuousComplianceNotification'


@dataclass
class ScheduleData:
	"""Scheduled email report notification

	:link  https://api-v2-docs.dome9.com/index.html?python#schemafalconetix-model-ruleengine-entities-continuouscompliancenotificationentity-reportscheduledata
	:param cron_expression: the schedule to issue the email report (in cron expression format)
	:type  cron_expression: str
	:param type: type of report; can be "Detailed", "Summary", "FullCsv" or "FullCsvZip"
	:type  type: str
	:param recipients: comma-separated list of email recipients
	:type  recipients: List[str]

	"""
	cron_expression: str
	type: str
	recipients: List[str]

	def __post_init__(self):
		report_types = [report_type.value for report_type in ScheduleDataReportType]
		if self.type not in report_types:
			raise UnsupportedScheduleDataReportType(f'report type must be one of the following {report_types}')


@dataclass
class ScheduledReport:
	"""Scheduled email report notification

	:link  https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-scheduledreportnotificationviewmodel
	:param email_sending_state: send schedule report of findings by email; can be "Enabled" or "Disabled"
	:type  email_sending_state: str
	:param schedule_data: Schedule data, if email_sending_state is Enabled, then schedule_data must be included
	:type  schedule_data: ScheduleData

	"""
	email_sending_state: str
	schedule_data: ScheduleData = None

	def __post_init__(self):
		APIUtils.check_is_valid_state(state=self.email_sending_state)


@dataclass
class EmailData:
	"""Email recipients

	:link  https://api-v2-docs.dome9.com/index.html?python#schemafalconetix-model-ruleengine-entities-continuouscompliancenotificationentity-emailnotificationdata
	:param recipients: comma-separated list of email recipients
	:type  1recipients: List[str]

	"""
	recipients: List[str]


@dataclass
class EmailPerFindingData:
	"""Email per finding notification

	:link  https://api-v2-docs.dome9.com/index.html?python#schemafalconetix-model-ruleengine-entities-continuouscompliancenotificationentity-emailperfindingnotificationdata
	:param recipients: comma-separated list of email recipients
	:type  recipients: List[str]
	:param notification_output_format: format of JSON block for finding; can be "JsonWithFullEntity", "JsonWithBasicEntity", or "PlainText".
	:type  notification_output_format: str

	"""
	recipients: List[str]
	notification_output_format: str

	def __post_init__(self):
		APIUtils.check_is_valid_notification_output_format(notification_output_format=self.notification_output_format)


@dataclass
class SNSData:
	"""Email per finding notification

	:link  https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-snsdatanotificationviewmodel
	:param sns_topic_arn: SNS topic ARN
	:type  sns_topic_arn: str
	:param sns_output_format: SNS output format; can be "JsonWithFullEntity", "JsonWithBasicEntity", or "PlainText"
	:type  sns_output_format: str

	"""
	sns_topic_arn: str
	sns_output_format: str

	def __post_init__(self):
		APIUtils.check_is_valid_notification_output_format(notification_output_format=self.sns_output_format)


@dataclass
class TicketingSystemData:
	"""Ticketing system

	:link  https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-ticketingsystemnotificationdataviewmodel
	:param system_type: System type; can be "ServiceOne", "Jira", or "PagerDuty"
	:type  system_type: str
	:param domain: serviceNow domain name (ServiceNow only)
	:type  domain: str
	:param user: User name (ServiceNow only)
	:type  user: str
	:param pass_: Password (ServiceNow only)
	:type  pass_: str
	:param project_key: Project key (Jira) or API Key (PagerDuty)
	:type  project_key: str
	:param issue_type: Issue type (Jira)
	:type  issue_type: str
	:param should_close_tickets: Ticketing system should close tickets when resolved (bool)
	:type  should_close_tickets: bool

	"""
	system_type: str
	domain: str
	user: str
	pass_: str
	project_key: str
	issue_type: str
	should_close_tickets: bool = True

	def __post_init__(self):
		system_types = [system_type.value for system_type in SystemType]
		if self.system_type not in system_types:
			raise UnsupportedNotificationSystemType(f'system type must be one of the following {system_types}')


@dataclass
class AWSSecurityHubIntegration:
	"""Ticketing system

	:link  https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-awssecurityhubintegrationnotificationviewmodel
	:param external_account_id (str): External account id
	:type  external_account_id: str
	:param region (str): AWS region
	:type  region: str

	"""
	external_account_id: str
	region: str


@dataclass
class WebhookData:
	"""Ticketing system

	:link  https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-webhooknotificationdataviewmodel
	:param url: HTTP endpoint URL
	:type  url: str
	:param http_method: HTTP method, "Post" by default.
	:type  http_method: str
	:param auth_method: Authentication method; "NoAuth" by default
	:type  auth_method: str
	:param username: Username in endpoint system
	:type  username: str
	:param password: Password in endpoint system
	:type  password: str
	:param format_type: Format for JSON block for finding; can be "Basic" or "ServiceNow"
	:type  format_type: str

	"""
	url: str
	http_method: str
	auth_method: str
	username: str
	password: str
	format_type: str

	def __post_init__(self):
		http_methods = [http_method.value for http_method in HttpMethod]
		if self.http_method not in http_methods:
			raise UnsupportedScheduleDataReportType(f'http method must be one of the following {http_methods}')

		auth_methods = [auth_method.value for auth_method in AuthMethod]
		if self.auth_method not in auth_methods:
			raise UnsupportedScheduleDataReportType(f'auth method must be one of the following {auth_methods}')

		format_types = [format_type.value for format_type in WebhookNotificationDataFormatType]
		if self.format_type not in format_types:
			raise UnsupportedNotificationOutputFormat(f'webhook format type output format must be one of the following {format_types}')


@dataclass
class ChangeDetection:
	"""Send changes in findings

	:link  https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-changedetectionnotificationviewmodel
	:param email_sending_state: Send email report of changes in findings; can be "Enabled" or "Disabled"
	:type  email_sending_state: str
	:param email_per_finding_sending_state: send separate email notification for each finding; can be "Enabled" or "Disabled"
	:type  email_per_finding_sending_state: str
	:param sns_sending_state: send by AWS SNS for each new finding; can be "Enabled" or "Disabled"
	:type  sns_sending_state: str
	:param external_ticket_creating_state: Send each finding to an external ticketing system; can be "Enabled" or "Disabled"
	:type  external_ticket_creating_state: str
	:param aws_security_hub_integration_state: send findings to AWS Secure Hub; can be "Enabled" or "Disabled"
	:type  aws_security_hub_integration_state: str
	:param webhook_integration_state: Send findings to an HTTP endpoint (webhook); can be "Enabled" or "Disabled".
	:type  webhook_integration_state: str
	:param email_data: If email_sending_stat is Enabled, email_data must be included
	:type  email_data: EmailData
	:param email_per_finding_data: If email_per_finding_sending_state is Enabled, email_per_finding_data must be included
	:type  email_per_finding_data: EmailPerFindingData
	:param sns_data: If sns_sending_state is Enabled, sns_data must be included:
	:type  sns_data: SNSData
	:param ticketing_system_data: if external_ticket_creating_state is Enabled, ticketing_system_data must be included
	:type  ticketing_system_data: TicketingSystemData
	:param aws_security_hub_integration: If aws_security_hub_integration_state is Enabled, aws_security_hub_integration must be included
	:type  aws_security_hub_integration: AWSSecurityHubIntegration
	:param webhook_data: If webhook_integration_state is Enabled, webhook_data must be included:
	:type  webhook_data: WebhookData

	"""
	email_sending_state: str
	email_per_finding_sending_state: str
	sns_sending_state: str
	external_ticket_creating_state: str
	aws_security_hub_integration_state: str
	webhook_integration_state: str
	email_data: EmailData = None
	email_per_finding_data: EmailPerFindingData = None
	sns_data: SNSData = None
	ticketing_system_data: TicketingSystemData = None
	aws_security_hub_integration: AWSSecurityHubIntegration = None
	webhook_data: WebhookData = None

	def __post_init__(self):
		APIUtils.check_is_valid_state(state=self.email_sending_state)
		APIUtils.check_is_valid_state(state=self.email_per_finding_sending_state)
		APIUtils.check_is_valid_state(state=self.sns_sending_state)
		APIUtils.check_is_valid_state(state=self.external_ticket_creating_state)
		APIUtils.check_is_valid_state(state=self.aws_security_hub_integration_state)
		APIUtils.check_is_valid_state(state=self.webhook_integration_state)


@dataclass
class GCPSecurityCommandCenterIntegration:
	"""Gcp security command center integration

	:link https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-gcpsecuritycommandcenterintegrationviewmodel
	:param state: Send findings to the GCP Security Command Center; can be "Enabled" or "Disabled"
	:type  state: str
	if state is Enabled, the following must be included:
		:param project_id: Gcp project id
		:type  project_id: str
		:param source_id: Gcp source id
		:type  source_id: str

	"""
	state: str
	project_id: str = None
	source_id: str = None

	def __post_init__(self):
		APIUtils.check_is_valid_state(state=self.state)


@dataclass
class ContinuousComplianceNotificationRequest(BaseDataclassRequest):
	"""Continuous compliance notification request

	:link  https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancenotificationgetviewmodel
	:param name: Notification name
	:type  name: str
	:param description: Description of the notification.
	:type  description: str
	:param change_detection: Send changes in findings
	:type  change_detection: ChangeDetection
	:param alerts_console: Send findings (also) to the Dome9 web app alerts console (Boolean); default is False.
	:type  alerts_console: bool
	:param scheduled_report: Scheduled email report notification
	:type  scheduled_report: ScheduledReport
	:param gcp_Security_command_center_integration: GCP security command center details
	:type  gcp_Security_command_center_integration: GCPSecurityCommandCenterIntegration

	"""
	name: str
	description: str
	change_detection: ChangeDetection
	alerts_console: bool = None
	scheduled_report: ScheduledReport = None
	gcp_Security_command_center_integration: GCPSecurityCommandCenterIntegration = None


class ContinuousComplianceNotification(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: ContinuousComplianceNotificationRequest) -> Dict:
		"""Create continuous compliance notification

		:link   https://api-v2-docs.dome9.com/index.html?python#continuouscompliancenotification_post
		:param  body: Details for the new continuous compliance notification
		:type   body: ContinuousComplianceNotificationRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancenotificationgetviewmodel
		:rtype  ContinuousComplianceNotificationGet

		"""
		return self._post(route=ContinuousComplianceNotificationConsts.CONTINUOUS_COMPLIANCE_NOTIFICATION.value, body=body)

	def get(self, continuous_compliance_notification_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get continuous compliance notification according to id

		:link    https://api-v2-docs.dome9.com/index.html?python#continuouscompliancenotification_get
		:param   continuous_compliance_notification_id: Continuous compliance notification id
		:type    continuous_compliance_notification_id: str
		:returns https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancenotificationgetviewmodel
		:rtype   ContinuousComplianceNotificationGet

		"""
		route = f'{ContinuousComplianceNotificationConsts.CONTINUOUS_COMPLIANCE_NOTIFICATION.value}/{continuous_compliance_notification_id}'
		return self._get(route=route)

	def update(self, continuous_compliance_notification_id: str, body: ContinuousComplianceNotificationRequest) -> Dict:
		"""Update continuous compliance notifications

		:link   https://api-v2-docs.dome9.com/index.html?python#continuouscompliancenotification_put
		:param  continuous_compliance_notification_id: Continuous compliance notification id
		:type   continuous_compliance_notification_id: str
		:param  body: Details for continuous compliance notifications
		:type   body: ContinuousComplianceNotificationRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancenotificationgetviewmodel
		:rtype  ContinuousComplianceNotificationGet

		"""
		route = f'{ContinuousComplianceNotificationConsts.CONTINUOUS_COMPLIANCE_NOTIFICATION.value}/{continuous_compliance_notification_id}'
		return self._put(route=route, body=body)

	def delete(self, continuous_compliance_notification_id: str) -> None:
		"""Delete continuous compliance notifications

		:param continuous_compliance_notification_id: Continuous compliance notifications
		:type  continuous_compliance_notification_id: str

		"""
		route = f'{ContinuousComplianceNotificationConsts.CONTINUOUS_COMPLIANCE_NOTIFICATION.value}/{continuous_compliance_notification_id}'
		return self._delete(route=route)

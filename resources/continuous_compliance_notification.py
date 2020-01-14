from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

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
	MAIN_ROUTE = 'Compliance/ContinuousComplianceNotification'


@dataclass
class ScheduleData:
	"""Scheduled email report notification

		Args:
			cron_expression (str): the schedule to issue the email report (in cron expression format)
			type (str): type of report; can be "Detailed", "Summary", "FullCsv" or "FullCsvZip"
			recipients (List[str]): comma-separated list of email recipients

	"""
	cron_expression: str
	type: str
	recipients: List[str]

	def __post_init__(self):
		reportTypes = [reportType.value for reportType in ScheduleDataReportType]
		if self.type not in reportTypes:
			raise UnsupportedScheduleDataReportType(f'report type must be one of the following {reportTypes}')


@dataclass
class ScheduledReport:
	"""Scheduled email report notification

		Args:
			email_sending_state (str): send schedule report of findings by email; can be "Enabled" or "Disabled"
			schedule_data (ScheduleData): if email_sending_state is Enabled, then schedule_data must be included

	"""
	email_sending_state: str
	schedule_data: ScheduleData = None

	def __post_init__(self):
		APIUtils.check_is_valid_state(state=self.email_sending_state)


@dataclass
class EmailData:
	"""Email recipients

		Args:
			recipients (List[str]): comma-separated list of email recipients

	"""
	recipients: List[str]


@dataclass
class EmailPerFindingData:
	"""Email per finding notification

		Args:
			recipients (List[str]): comma-separated list of email recipients
			notification_output_format (str): format of JSON block for finding; can be "JsonWithFullEntity", "JsonWithBasicEntity", or "PlainText".

	"""
	recipients: List[str]
	notification_output_format: str

	def __post_init__(self):
		APIUtils.check_is_valid_notification_output_format(notification_output_format=self.notification_output_format)


@dataclass
class SNSData:
	"""Email per finding notification

		Args:
			sns_topic_arn (str): SNS topic ARN
			sns_output_format (str): SNS output format; can be "JsonWithFullEntity", "JsonWithBasicEntity", or "PlainText"

	"""
	sns_topic_arn: str
	sns_output_format: str

	def __post_init__(self):
		APIUtils.check_is_valid_notification_output_format(notification_output_format=self.sns_output_format)


@dataclass
class TicketingSystemData:
	"""Ticketing system

		Args:
			system_type (str): System type; can be "ServiceOne", "Jira", or "PagerDuty"
			domain (str): serviceNow domain name (ServiceNow only)
			user (str): User name (ServiceNow only)
			Pass (str): Password (ServiceNow only)
			project_key (str): Project key (Jira) or API Key (PagerDuty)
			issue_type (str): Issue type (Jira)
			should_close_tickets (bool): Ticketing system should close tickets when resolved (bool)

	"""
	system_type: str
	domain: str
	user: str
	Pass: str
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

		Args:
			external_account_id (str): External account id
			region (str): AWS region

	"""
	external_account_id: str
	region: str


@dataclass
class WebhookData:
	"""Ticketing system

		Args:
			url (str): HTTP endpoint URL
			http_method (str): HTTP method, "Post" by default.
			auth_method (str): Authentication method; "NoAuth" by default
			username (str): Username in endpoint system
			password (str): Password in endpoint system
			format_type (str): Format for JSON block for finding; can be "Basic" or "ServiceNow"

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

		Args:
			email_sending_state (str): Send email report of changes in findings; can be "Enabled" or "Disabled"
			email_per_finding_sending_state (str): send separate email notification for each finding; can be "Enabled" or "Disabled"
			sns_sending_state (str): send by AWS SNS for each new finding; can be "Enabled" or "Disabled"
			external_ticket_creating_state (str): Send each finding to an external ticketing system; can be "Enabled" or "Disabled"
			aws_security_hub_integration_state (str): send findings to AWS Secure Hub; can be "Enabled" or "Disabled"
			webhook_integration_state (str): Send findings to an HTTP endpoint (webhook); can be "Enabled" or "Disabled".
			email_data (EmailData): If email_sending_stat is Enabled, email_data must be included
			email_per_finding_data (EmailPerFindingData): If email_per_finding_sending_state is Enabled, email_per_finding_data must be included
			sns_data (SNSData): If sns_sending_state is Enabled, sns_data must be included:
			ticketing_system_data (TicketingSystemData): if external_ticket_creating_state is Enabled, ticketing_system_data must be included
			aws_security_hub_integration (AWSSecurityHubIntegration): If aws_security_hub_integration_state is Enabled, aws_security_hub_integration must be included
			webhook_data (WebhookData): If webhook_integration_state is Enabled, webhook_data must be included:

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
	state: str
	project_id: str
	source_id: str


@dataclass
class ContinuousComplianceNotificationRequest(BaseDataclassRequest):
	"""Continuous compliance notification request

		Args:
			name (str): Notification name
			description (str): Description of the notification.
			change_detection (ChangeDetection): Send changes in findings
			alerts_console (bool): Send findings (also) to the Dome9 web app alerts console (Boolean); default is False.
			scheduled_report (ScheduledReport): Scheduled email report notification
			gcp_Security_command_center_integration (GCPSecurityCommandCenterIntegration): GCP security command center details

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

		:param body: Details for the new continuous compliance notification
		:type body: ContinuousComplianceNotificationRequest
		:returns: Dict that has metadata for the created continuous compliance notification

		"""
		return self._post(route=ContinuousComplianceNotificationConsts.MAIN_ROUTE.value, body=body)

	def get(self, continuous_compliance_notification_id: str) -> Dict:
		"""Get continuous compliance notification according to id

		:param continuous_compliance_notification_id: Continuous compliance notification id
		:type continuous_compliance_notification_id: str
		:returns: Dict that has metadata for continuous compliance notification

		"""
		route = f'{ContinuousComplianceNotificationConsts.MAIN_ROUTE.value}/{continuous_compliance_notification_id}'
		return self._get(route=route)

	def get_all(self) -> List[Dict]:
		"""Get all continuous compliance notifications in dome9

		:returns: List of dicts that has metadata for all continuous compliance notifications

		"""
		return self._get(route=ContinuousComplianceNotificationConsts.MAIN_ROUTE.value)

	def update(self, continuous_compliance_notification_id: str, body: ContinuousComplianceNotificationRequest) -> Dict:
		"""Update continuous compliance notifications

		:param continuous_compliance_notification_id: Continuous compliance notification id
		:type continuous_compliance_notification_id: str
		:param body: Details for continuous compliance notifications
		:type body: ContinuousComplianceNotificationRequest

		:returns: Dict that has metadata for continuous compliance notifications

		"""
		route = f'{ContinuousComplianceNotificationConsts.MAIN_ROUTE.value}/{continuous_compliance_notification_id}'
		return self._put(route=route, body=body)

	def delete(self, continuous_compliance_notification_id: str) -> None:
		"""Delete continuous compliance notifications

		:param continuous_compliance_notification_id: Continuous compliance notifications
		:type continuous_compliance_notification_id: str
		:returns: None

		"""
		route = f'{ContinuousComplianceNotificationConsts.MAIN_ROUTE.value}/{continuous_compliance_notification_id}'
		return self._delete(route=route)

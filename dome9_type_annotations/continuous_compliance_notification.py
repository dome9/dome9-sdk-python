from typing import Dict, List, Union

from resources.continuous_compliance_notification import ContinuousComplianceNotification, ContinuousComplianceNotificationRequest


class continuous_compliance_notification(ContinuousComplianceNotification):

	@classmethod
	def create(cls, body: ContinuousComplianceNotificationRequest) -> Dict:
		"""Create continuous compliance notification

		:link   https://api-v2-docs.dome9.com/index.html?python#continuouscompliancenotification_post
		:param  body: Details for the new continuous compliance notification
		:type   body: ContinuousComplianceNotificationRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancenotificationgetviewmodel
		:rtype  ContinuousComplianceNotificationGet

		"""
		pass

	@classmethod
	def get(cls, continuous_compliance_notification_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get continuous compliance notification according to id

		:link    https://api-v2-docs.dome9.com/index.html?python#continuouscompliancenotification_get
		:param   continuous_compliance_notification_id: Continuous compliance notification id
		:type    continuous_compliance_notification_id: str
		:returns https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancenotificationgetviewmodel
		:rtype   ContinuousComplianceNotificationGet

		"""
		pass

	@classmethod
	def update(cls, continuous_compliance_notification_id: str, body: ContinuousComplianceNotificationRequest) -> Dict:
		"""Update continuous compliance notifications

		:link   https://api-v2-docs.dome9.com/index.html?python#continuouscompliancenotification_put
		:param  continuous_compliance_notification_id: Continuous compliance notification id
		:type   continuous_compliance_notification_id: str
		:param  body: Details for continuous compliance notifications
		:type   body: ContinuousComplianceNotificationRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancenotificationgetviewmodel
		:rtype  ContinuousComplianceNotificationGet

		"""
		pass

	@classmethod
	def delete(cls, continuous_compliance_notification_id: str) -> None:
		"""Delete continuous compliance notifications

		:param continuous_compliance_notification_id: Continuous compliance notifications
		:type  continuous_compliance_notification_id: str

		"""
		pass

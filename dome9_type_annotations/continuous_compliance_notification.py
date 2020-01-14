from typing import Dict, List

from resources.continuous_compliance_notification import ContinuousComplianceNotification as BaseAzureCloudAccount, ContinuousComplianceNotificationRequest


class continuous_compliance_notification(BaseAzureCloudAccount):

	@classmethod
	def create(cls, body: ContinuousComplianceNotificationRequest) -> Dict:
		pass

	@classmethod
	def get(cls, continuous_compliance_notification_id: str) -> Dict:
		pass

	@classmethod
	def get_all(cls) -> List[Dict]:
		pass

	@classmethod
	def update(cls, continuous_compliance_notification_id: str, body: ContinuousComplianceNotificationRequest) -> Dict:
		pass

	@classmethod
	def delete(cls, continuous_compliance_notification_id: str) -> None:
		pass

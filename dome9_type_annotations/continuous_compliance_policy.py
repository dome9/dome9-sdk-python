from typing import Dict, List

from resources.continuous_compliance_policy import ContinuousCompliancePolicyRequest
from resources.continuous_compliance_policy import ContinuousCompliancePolicy as BaseAwsCloudAccount


class continuous_compliance_policy(BaseAwsCloudAccount):

	@classmethod
	def create(cls, body: ContinuousCompliancePolicyRequest) -> Dict:
		pass

	@classmethod
	def get(cls, continuous_compliance_policy_id: str) -> Dict:
		pass

	@classmethod
	def get_all(cls) -> List[Dict]:
		pass

	@classmethod
	def update(cls, continuous_compliance_policy_id: str, body: ContinuousCompliancePolicyRequest) -> Dict:
		pass

	@classmethod
	def delete(cls, continuous_compliance_policy_id: str) -> None:
		pass

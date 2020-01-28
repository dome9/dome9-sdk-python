from typing import Dict, List, Union

from resources.continuous_compliance_policy import ContinuousCompliancePolicyRequest
from resources.continuous_compliance_policy import ContinuousCompliancePolicy as ContinuousCompliancePolicy


class continuous_compliance_policy(ContinuousCompliancePolicy):

	@classmethod
	def create(cls, body: ContinuousCompliancePolicyRequest) -> Dict:
		"""Create continuous compliance policy

		:link   https://api-v2-docs.dome9.com/index.html?python#continuouscompliancepolicy_post
		:param  body: Details for the new continuous compliance policy
		:type   body: ContinuousCompliancePolicyRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancepolicygetviewmodel
		:rtype  ContinuousCompliancePolicyGet

		"""
		pass

	@classmethod
	def get(cls, continuous_compliance_policy_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get information for continuous compliance policy

		:link    https://api-v2-docs.dome9.com/index.html?python#continuouscompliancepolicy_get
		:param   continuous_compliance_policy_id: Continuous compliance policy id
		:type    continuous_compliance_policy_id: str
		:returns https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancepolicygetviewmodel
		:rtype   ContinuousCompliancePolicyGet

		"""
		pass

	@classmethod
	def update(cls, continuous_compliance_policy_id: str, body: ContinuousCompliancePolicyRequest) -> Dict:
		"""Update continuous compliance policy

		:link   https://api-v2-docs.dome9.com/index.html?python#continuouscompliancepolicy_put
		:param  body: Details for continuous compliance policy
		:type   body: ContinuousCompliancePolicyRequest
		:param  continuous_compliance_policy_id: Continuous compliance policy id
		:type   continuous_compliance_policy_id: str
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancepolicygetviewmodel
		:rtype  ContinuousCompliancePolicyGet

		"""
		pass

	@classmethod
	def delete(cls, continuous_compliance_policy_id: str) -> None:
		"""Delete continuous compliance policy

		:param  continuous_compliance_policy_id: Continuous compliance policy id
		:type   continuous_compliance_policy_id: str
		:return None

		"""
		pass

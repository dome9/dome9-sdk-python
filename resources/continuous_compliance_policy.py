from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union

from dome9 import Client, Dome9Resource, BaseDataclassRequest


class ContinuousCompliancePolicyConsts(Enum):
	CONTINUOUS_COMPLIANCE_POLICY = 'Compliance/ContinuousCompliancePolicy'


@dataclass
class ContinuousCompliancePolicyRequest(BaseDataclassRequest):
	"""AWS security group request

	:link: https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancepolicypostviewmodel
	:param cloud_account_id: Cloud account id
	:type  cloud_account_id: str
	:param external_account_id: External account id
	:type  external_account_id: str
	:param cloud_account_type: The cloud account provider ("AWS", "Azure", "Google")
	:type  cloud_account_type: str
	:param bundle_id: The bundle id for the bundle that will be used in the policy
	:type  bundle_id: str
	:param notification_ids: The notification policy id's for the policy
	:type  notification_ids: List[str]

	"""
	cloud_account_id: str
	external_account_id: str
	cloud_account_type: str
	bundle_id: str
	notification_ids: List[str]


class ContinuousCompliancePolicy(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client=client)

	def create(self, body: ContinuousCompliancePolicyRequest) -> Dict:
		"""Create continuous compliance policy

		:link   https://api-v2-docs.dome9.com/index.html?python#continuouscompliancepolicy_post
		:param  body: Details for the new continuous compliance policy
		:type   body: ContinuousCompliancePolicyRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancepolicygetviewmodel
		:rtype  ContinuousCompliancePolicyGet

		"""
		return self._post(route=ContinuousCompliancePolicyConsts.CONTINUOUS_COMPLIANCE_POLICY.value, body=body)

	def get(self, continuous_compliance_policy_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get information for continuous compliance policy

		:link    https://api-v2-docs.dome9.com/index.html?python#continuouscompliancepolicy_get
		:param   continuous_compliance_policy_id: Continuous compliance policy id
		:type    continuous_compliance_policy_id: str
		:returns https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancepolicygetviewmodel
		:rtype   ContinuousCompliancePolicyGet

		"""
		route = f'{ContinuousCompliancePolicyConsts.CONTINUOUS_COMPLIANCE_POLICY.value}/{continuous_compliance_policy_id}'
		return self._get(route=route)

	def update(self, continuous_compliance_policy_id: str, body: ContinuousCompliancePolicyRequest) -> Dict:
		"""Update continuous compliance policy

		:link   https://api-v2-docs.dome9.com/index.html?python#continuouscompliancepolicy_put
		:param  body: Details for continuous compliance policy
		:type   body: ContinuousCompliancePolicyRequest
		:param  continuous_compliance_policy_id: Continuous compliance policy id
		:type   continuous_compliance_policy_id: str
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-compliance-continuouscompliance-continuouscompliancepolicygetviewmodel
		:rtype  ContinuousCompliancePolicyGet

		"""
		route = f'{ContinuousCompliancePolicyConsts.CONTINUOUS_COMPLIANCE_POLICY.value}/{continuous_compliance_policy_id}'
		return self._put(route=route, body=body)

	def delete(self, continuous_compliance_policy_id: str) -> None:
		"""Delete continuous compliance policy

		:param  continuous_compliance_policy_id: Continuous compliance policy id
		:type   continuous_compliance_policy_id: str
		:return None

		"""
		route = f'{ContinuousCompliancePolicyConsts.CONTINUOUS_COMPLIANCE_POLICY.value}/{continuous_compliance_policy_id}'
		return self._delete(route=route)

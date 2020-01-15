from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from dome9 import Client, Dome9Resource, BaseDataclassRequest


class ContinuousCompliancePolicyConsts(Enum):
	MAIN_ROUTE = 'Compliance/ContinuousCompliancePolicy'


@dataclass
class ContinuousCompliancePolicyRequest(BaseDataclassRequest):
	"""AWS security group request

		Args:
			cloud_account_id (str): Cloud account id
			external_account_id (str): External account id
			cloud_account_type (str): The cloud account provider ("AWS", "Azure", "Google")
			bundle_id (str): The bundle id for the bundle that will be used in the policy
			notification_ids (List[str]): The notification policy id's for the policy

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

		:param body: Details for the new continuous compliance policy
		:type body: ContinuousCompliancePolicyRequest
		:returns: Dict that has metadata for the created continuous compliance policy

		"""
		return self._post(route=ContinuousCompliancePolicyConsts.MAIN_ROUTE.value, body=body)

	def get(self, continuous_compliance_policy_id: str) -> Dict:
		"""Get information for continuous compliance policy

		:param continuous_compliance_policy_id: Continuous compliance policy id
		:type continuous_compliance_policy_id: str
		:returns: Dict that has metadata for continuous compliance policy

		"""
		route = f'{ContinuousCompliancePolicyConsts.MAIN_ROUTE.value}/{continuous_compliance_policy_id}'
		return self._get(route=route)

	def get_all(self) -> List[Dict]:
		"""Get all continuous compliance policies

		:returns: List of dicts that has metadata for all the continuous compliance policies

		"""
		return self._get(route=ContinuousCompliancePolicyConsts.MAIN_ROUTE.value)

	def update(self, continuous_compliance_policy_id: str, body: ContinuousCompliancePolicyRequest) -> Dict:
		"""Update continuous compliance policy

		:param body: Details for continuous compliance policy
		:type body: ContinuousCompliancePolicyRequest
		:param continuous_compliance_policy_id: Continuous compliance policy id
		:type continuous_compliance_policy_id: str

		:returns: Dict that has metadata for updated continuous compliance policy

		"""
		route = f'{ContinuousCompliancePolicyConsts.MAIN_ROUTE.value}/{continuous_compliance_policy_id}'
		return self._put(route=route, body=body)

	def delete(self, continuous_compliance_policy_id: str) -> None:
		"""Delete continuous compliance policy

		:param continuous_compliance_policy_id: Continuous compliance policy id
		:type continuous_compliance_policy_id: str
		:returns: None

		"""
		route = f'{ContinuousCompliancePolicyConsts.MAIN_ROUTE.value}/{continuous_compliance_policy_id}'
		return self._delete(route=route)

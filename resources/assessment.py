from dataclasses import dataclass
from enum import Enum

from dome9 import Dome9Resource, Client, BaseDataclassRequest


class AssessmentConsts(Enum):
	MAIN_ROUTE = 'assessment/bundleV2'


@dataclass
class RunBundleRequest(BaseDataclassRequest):
	"""AWS cloud account credentials

		Args:
			id (str): Bundle id
			cloud_account_id (str): cloud account id
			region (str): aws region, by default all regions

	"""
	id: str
	cloud_account_id: str
	region: str = None


class Assessment(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def run_bundle(self, body: RunBundleRequest):
		"""Create (onboard) aws cloud account

		:param body: Details for the bundle that we want to run
		:type body: RunBundleRequest
		:returns: Dict the running bundle

		"""
		return self._post(route=AssessmentConsts.MAIN_ROUTE.value, body=body)

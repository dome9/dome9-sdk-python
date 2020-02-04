from dataclasses import dataclass
from enum import Enum

from dome9 import Dome9Resource, Client, BaseDataclassRequest


class AssessmentConsts(Enum):
	ASSESSMENT_BUNDLE_V2 = 'assessment/bundleV2'


@dataclass
class AssessmentBundleRequest(BaseDataclassRequest):
	"""AssessmentBundleRequest

	:link   https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-models-assessmentbundlerequestviewmodel
	:param  id: the bundle id
	:type   id: str
	:param  cloud_account_id: account id on cloud provider (AWS, Azure, GCP)
	:type   cloud_account_id: str
	:param  region: cloud region for the account
	:type   region: str
	:param dome9_cloud_account_id: The Dome9 account id
	:type dome9_cloud_account_id: str
	:param external_cloud_account_id: account id on cloud provider (AWS, Azure, GCP)
	:type external_cloud_account_id: str
	"""
	id: str
	cloud_account_id: str
	region: str = None
	dome9_cloud_account_id: str = None
	external_cloud_account_id: str = None

class Assessment(Dome9Resource):
	"""Assessment

	"""
	def __init__(self, client: Client):
		super().__init__(client)

	def run_bundle(self, body: AssessmentBundleRequest):
		"""Run an assessment on a cloud environment using a bundle (V2)

		:link   https://api-v2-docs.dome9.com/index.html#Dome9-API-Assessment
		:param  body: The assessment request block
		:type   body: AssessmentBundleRequest
		:return https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-models-assessmentresultviewmodel
		:rtype  AssessmentResult

		"""
		return self._post(route=AssessmentConsts.ASSESSMENT_BUNDLE_V2.value, body=body)

from typing import Dict

from resources.assessment import Assessment as BaseAwsCloudAccount, AssessmentBundleRequest


class assessment(BaseAwsCloudAccount):

	@classmethod
	def run_bundle(cls, body: AssessmentBundleRequest) -> Dict:
		"""Run an assessment on a cloud environment using a bundle (V2)

		:link   https://api-v2-docs.dome9.com/index.html#Dome9-API-Assessment
		:param  body: The assessment request block
		:type   body: AssessmentBundleRequest
		:return https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-models-assessmentresultviewmodel
		:rtype  AssessmentResult

		"""
		pass

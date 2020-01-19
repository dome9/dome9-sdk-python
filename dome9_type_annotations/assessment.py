from typing import Dict

from resources.assessment import Assessment as BaseAwsCloudAccount, RunBundleRequest


class assessment(BaseAwsCloudAccount):

	@classmethod
	def run_bundle(cls, body: RunBundleRequest) -> Dict:
		pass

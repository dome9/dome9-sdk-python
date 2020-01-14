from typing import Dict, List

from resources.rule_bundle import RuleBundle as BaseAwsCloudAccount
from resources.rule_bundle import RuleBundleRequest


class rule_bundle(BaseAwsCloudAccount):

	@classmethod
	def create(cls, body: RuleBundleRequest) -> Dict:
		pass

	@classmethod
	def get(cls, rule_bundle_id: str) -> Dict:
		pass

	@classmethod
	def get_all(cls) -> List:
		pass

	@classmethod
	def update(cls, body: RuleBundleRequest) -> Dict:
		pass

	@classmethod
	def delete(cls, rule_bundle_id: str) -> None:
		pass

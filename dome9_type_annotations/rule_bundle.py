from typing import Dict, List, Union

from resources.rule_bundle import RuleBundle as BaseRuleBundle, RuleBundleRequest


class rule_bundle(BaseRuleBundle):

	@classmethod
	def create(cls, body: RuleBundleRequest) -> Dict:
		"""Create rule bundle

		:param  body: Details for the new rule bundle
		:type   body: RuleBundleRequest
		:return Metadata for the created rule bundle
		:rtype  Dict

		"""
		pass

	@classmethod
	def get(cls, rule_bundle_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get information for rule bundle

		:param  rule_bundle_id: Rule bundle id
		:type   rule_bundle_id: str
		:return Metadata for the rule bundle
		:rtype  Dict or List[Dict]

		"""
		pass

	@classmethod
	def update(cls, body: RuleBundleRequest) -> Dict:
		"""Update rule bundle

		:param  body: Details for rule bundle
		:type   body: RuleBundleRequest
		:return Metadata for updated rule bundle
		:rtype  Dict

		"""
		pass

	@classmethod
	def delete(cls, rule_bundle_id: str) -> None:
		"""Delete aws cloud account

		:param rule_bundle_id: Rule bundle id
		:type  rule_bundle_id: str

		"""
		pass

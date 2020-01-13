from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

from loguru import logger

from dome9 import Dome9Resource, Client, BaseDataclassRequest
from dome9.consts import CloudVendors
from dome9.exceptions import UnsupportedRuleEntitySeverity, UnsupportedCloudVendor


class RuleEntitySeverity(Enum):
	LOW = 'Low'
	MEDIUM = 'Medium'
	HIGH = 'High'


class RuleBundleConsts(Enum):
	MAIN_ROUTE = 'CompliancePolicy'


@dataclass
class Rule:
	"""Restricted iam entities request

		Args:
			name (str): Rule name
			logic (str): The GSL statement for the rule
			severity (str): Rule severity (High/Medium/Low)
			description (str): Description of the rule
			remediation (str): Remediation text for the rule
			compliance_tag (str): Compliance section for the rule

	"""
	name: str
	logic: str
	severity: str
	description: str = None
	remediation: str = None
	compliance_tag: str = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		rule_entity_severities = [rule_severity.value for rule_severity in RuleEntitySeverity]
		if self.severity not in rule_entity_severities:
			raise UnsupportedRuleEntitySeverity(f'rule entity severity must be one of the following {rule_entity_severities}')


@dataclass
class RuleBundleRequest(BaseDataclassRequest):
	"""Restricted iam entities request

		Args:
			name (str): Rule bundle name
			cloud_vendor (str): Cloud provider on which the rule will be run
			description (str): Description of the bundle
			rules (List[Rule]): List of rules in the bundle
			language (str): Language of the text (default, 'en' - English)
			id (str): Rule bundle id, relevant in update

	"""
	name: str
	cloud_vendor: str
	description: str = None
	rules: List[Rule] = None
	language: str = None
	id: str = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		cloud_vendors = [cloud_vendor.value for cloud_vendor in CloudVendors]
		if self.cloud_vendor not in cloud_vendors:
			raise UnsupportedCloudVendor(f'cloud vendor must be one of the following {cloud_vendors}')


class RuleBundle(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client=client)

	def create(self, body: RuleBundleRequest) -> Dict:
		"""Create rule bundle

		:param body: Details for the new rule bundle
		:type body: RuleBundleRequest
		:returns: Dict that has metadata for the created rule bundle

		"""
		return self._post(route=RuleBundleConsts.MAIN_ROUTE.value, body=body)

	def get(self, rule_bundle_id: str) -> Dict:
		"""Get information for rule bundle

		:param rule_bundle_id: Rule bundle id
		:type rule_bundle_id: str
		:returns: Dict that has metadata for the rule bundle

		"""
		route = f'{RuleBundleConsts.MAIN_ROUTE.value}/{rule_bundle_id}'
		return self._get(route=route)

	def get_all_rule_bundles(self) -> List:
		"""Get all rule bundles

		:returns: List of dicts that has metadata for all the rule bundles

		"""
		return self._get(route=RuleBundleConsts.MAIN_ROUTE.value)

	def update(self, body: RuleBundleRequest):
		"""Update rule bundle

		:param body: Details for rule bundle
		:type body: RuleBundleRequest

		:returns: Dict that has metadata for updated rule bundle

		"""
		return self._put(route=RuleBundleConsts.MAIN_ROUTE.value, body=body)

	def delete(self, rule_bundle_id: str) -> None:
		"""Delete aws cloud account

		:param rule_bundle_id: Rule bundle id
		:type rule_bundle_id: str
		:returns: None

		"""
		route = f'{RuleBundleConsts.MAIN_ROUTE.value}/{rule_bundle_id}'
		return self._delete(route=route)

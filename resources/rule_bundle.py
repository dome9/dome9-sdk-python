from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Union

from loguru import logger

from dome9 import Dome9Resource, Client, BaseDataclassRequest
from dome9.consts import CloudVendors
from dome9.exceptions import UnsupportedRuleEntitySeverity, UnsupportedCloudVendor


class RuleEntitySeverity(Enum):
	LOW = 'Low'
	MEDIUM = 'Medium'
	HIGH = 'High'


class RuleBundleConsts(Enum):
	COMPLIANCE_POLICY = 'CompliancePolicy'


@dataclass
class Rule:
	"""Restricted iam entities request

	:param name: Rule name
	:type  name: str
	:param logic: The GSL statement for the rule
	:type  logic: str
	:param severity: Rule severity (High/Medium/Low)
	:type  severity: str
	:param description: Description of the rule
	:type  description: str
	:param remediation: Remediation text for the rule
	:type  remediation: str
	:param compliance_tag: Compliance section for the rule
	:type  compliance_tag: str

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

	:param name: Rule bundle name
	:type  name: str
	:param cloud_vendor: Cloud provider on which the rule will be run
	:type  cloud_vendor: str
	:param description: Description of the bundle
	:type  description: str
	:param rules: List of rules in the bundle
	:type  rules: List
	:param language: Language of the text (default, 'en' - English)
	:type  language: str
	:param id: Rule bundle id, relevant in update
	:type  id: str

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

		:param  body: Details for the new rule bundle
		:type   body: RuleBundleRequest
		:return Metadata for the created rule bundle
		:rtype  Dict

		"""
		return self._post(route=RuleBundleConsts.COMPLIANCE_POLICY.value, body=body)

	def get(self, rule_bundle_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get information for rule bundle

		:param  rule_bundle_id: Rule bundle id
		:type   rule_bundle_id: str
		:return Metadata for the rule bundle
		:rtype  Dict or List[Dict]

		"""
		route = f'{RuleBundleConsts.COMPLIANCE_POLICY.value}/{rule_bundle_id}'
		return self._get(route=route)

	def update(self, body: RuleBundleRequest):
		"""Update rule bundle

		:param  body: Details for rule bundle
		:type   body: RuleBundleRequest
		:return Metadata for updated rule bundle
		:rtype  Dict

		"""
		return self._put(route=RuleBundleConsts.COMPLIANCE_POLICY.value, body=body)

	def delete(self, rule_bundle_id: str) -> None:
		"""Delete aws cloud account

		:param rule_bundle_id: Rule bundle id
		:type  rule_bundle_id: str

		"""
		route = f'{RuleBundleConsts.COMPLIANCE_POLICY.value}/{rule_bundle_id}'
		return self._delete(route=route)

#!/usr/bin/env python
import argparse
import json
from typing import Dict

from loguru import logger

from dome9_type_annotations.client import Client
from resources.assessment import AssessmentBundleRequest
from resources.rule_bundle import RuleBundleRequest


class UpdateRuleset(object):

	def __init__(self, args: argparse.Namespace):
		self.args: Dict = vars(args)
		self.d9_client = Client(access_id=args.dome9ApiKeyID, secret_key=args.dome9ApiKeySecret)

	def update_bundle(self) -> None:
		logger.info(f'''loading bundle from {self.args['rulesetJsonPath']}''')

		with open(self.args['rulesetJsonPath']) as jsonFile:
			rule_bundle_object = json.load(jsonFile)

		logger.info(f'''updating bundle {self.args['bundleID']}''')
		payload = RuleBundleRequest(id=self.args['bundleID'],
			name=rule_bundle_object['name'],
			cloud_vendor=rule_bundle_object['cloudVendor'],
			description=rule_bundle_object['description'],
			rules=rule_bundle_object['rules'],
			language=rule_bundle_object['language'])
		self.d9_client.rule_bundle.update(body=payload)

	def run_assessment(self) -> None:
		bundle = AssessmentBundleRequest(id=self.args['bundleID'], cloud_account_id=self.args['cloudAccountID'])
		logger.info(f'''running assessment bundle id {self.args['bundleID']}''')
		bundle_result = self.d9_client.assessment.run_bundle(body=bundle)
		logger.info(f'bundle result is: {json.dumps(bundle_result)}')

	def main(self) -> None:
		self.update_bundle()
		self.run_assessment()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='Given the bundleId and file with ruleset in Json format, updates the bundle and runs assessment')

	useExample = '--dome9ApiKeyID 111111-2222-3333-3333-3333333 --dome9ApiKeySecret qwerrtyy --rulesetJsonPath ruleset.json --bundleID 11111 --cloudAccountID 11111111111'
	parser.epilog = f'Example of use: {__file__} {useExample}'

	parser.add_argument('--dome9ApiKeyID', required=True, type=str, help='dome9 api key')
	parser.add_argument('--dome9ApiKeySecret', required=True, type=str, help='dome9 secret key')
	parser.add_argument('--bundleID', required=True, type=str, help='dome9 bundle id')
	parser.add_argument('--rulesetJsonPath', required=True, type=str, help='location for ruleset json file')
	parser.add_argument('--cloudAccountID', required=True, type=str, help='dome9 external account id')

	arguments = parser.parse_args()
	updateRuleset = UpdateRuleset(arguments)
	updateRuleset.main()

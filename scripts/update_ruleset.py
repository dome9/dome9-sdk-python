#!/usr/bin/env python
import argparse
import json
import uuid

from dome9_type_annotations.client import Client
from resources.assessment import AssessmentBundleRequest
from resources.rule_bundle import RuleBundleRequest


class UpdateRuleset(object):

	@staticmethod
	def get_json(path):
		with open(path) as jsonFile:
			return json.load(jsonFile)

	@staticmethod
	def create_bundle_request(requestId, cloudAccountID, bundleID):
		return {'id': bundleID, 'cloudAccountId': cloudAccountID, 'requestId': requestId}

	def __init__(self, args):
		self.args = args
		self.d9_client = Client(access_id=args.dome9ApiKeyID, secret_key=args.dome9ApiKeySecret)

	def update_bundle(self):
		print(f'loading bundle from {self.args.rulesetJsonPath}')
		rule_bundle_object = self.get_json(self.args.rulesetJsonPath)
		print(f'updating bundle {self.args.bundleID}')
		payload = RuleBundleRequest(id=self.args.bundleID,
			name=rule_bundle_object['name'],
			cloud_vendor=rule_bundle_object['cloudVendor'],
			description=rule_bundle_object['description'],
			rules=rule_bundle_object['rules'],
			language=rule_bundle_object['language'])
		self.d9_client.rule_bundle.update(body=payload)

	def run_assessment(self):
		bundle = AssessmentBundleRequest(id=self.args.bundleID, cloud_account_id=self.args.cloudAccountID)
		print(f'running assessment bundle id {self.args.bundleID}')
		bundle_result = self.d9_client.assessment.run_bundle(body=bundle)
		bundle_result_str = json.dumps(bundle_result)
		print('bundle result is\n{}'.format(bundle_result_str))

	def main(self):
		self.update_bundle()
		self.run_assessment()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='Given the bundleId and file with ruleset in Json format, updates the bundle and runs assessment')

	useExample = '--dome9ApiKeyID 111111-2222-3333-3333-3333333 --dome9ApiKeySecret qwerrtyy --rulesetJsonPath ruleset.json --bundleID 11111 --cloudAccountID 11111111111'
	parser.epilog = 'Example of use: {} {}'.format(__file__, useExample)

	parser.add_argument('--dome9ApiKeyID', required=True, type=str, help='(required) Dome9 Api key')
	parser.add_argument('--dome9ApiKeySecret', required=True, type=str, help='(required) Dome9 secret key')
	parser.add_argument('--bundleID', required=True, type=str, help='(required) Dome9 bundle ID')
	parser.add_argument('--rulesetJsonPath', required=True, type=str, help='(required) Location for ruleset json file')
	parser.add_argument('--cloudAccountID', required=True, type=str, help='(required) Dome9 external account ID')

	arguments = parser.parse_args()
	updateRuleset = UpdateRuleset(arguments)
	updateRuleset.main()

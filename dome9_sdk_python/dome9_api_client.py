import json

from dome9_sdk_python import Dome9ApiSDK


class Dome9ApiClient(Dome9ApiSDK):

	def getCloudSecurityGroupsInRegion(self, region, names=False):
		groupID = 'name' if names else 'id'
		return [secGrp[groupID] for secGrp in self.getAwsSecurityGroups() if secGrp['regionId'] == region]

	def getCloudSecurityGroupsIDsOfVpc(self, vpcID):
		return [secGrp['id'] for secGrp in self.getAwsSecurityGroups() if secGrp['vpcId'] == vpcID]

	def getCloudSecurityGroupIDsOfVpc(self, vpcID):
		return [secGrp['id'] for secGrp in self.getAwsSecurityGroups() if secGrp['vpcId'] == vpcID]

	def getCloudSecurityGroupsIdsOfAccount(self, accountID):
		return [secGrp['externalId'] for secGrp in self.getAwsSecurityGroups() if secGrp['awsAccountId'] == accountID]

	def setCloudRegionsProtectedMode(self, ID, protectionMode, regions='all'):
		if protectionMode not in Dome9ApiSDK.REGION_PROTECTION_MODES:
			raise ValueError('Valid modes are: {}'.format(Dome9ApiSDK.REGION_PROTECTION_MODES))

		allUsersRegions = self.getCloudAccountRegions(ID=ID)
		if regions == 'all':
			cloudAccountRegions = allUsersRegions
		else:
			if not set(regions).issubset(allUsersRegions):
				raise Exception('requested regions:{} are not a valid regions, available:{}'.format(regions, allUsersRegions))
			cloudAccountRegions = regions

		for region in cloudAccountRegions:
			data = json.dumps(
				{'externalAccountNumber': ID, 'data': {'region': region, 'newGroupBehavior': protectionMode}})
			print('updating data: {}'.format(data))
			self.put(route='cloudaccounts/region-conf', payload=data)

	def setCloudSecurityGroupsProtectionModeInRegion(self, region, protectionMode):
		secGrpsRegion = self.getCloudSecurityGroupsInRegion(region=region)
		if not secGrpsRegion:
			raise ValueError('got 0 security groups!')
		for secGrpID in secGrpsRegion:
			self.setCloudSecurityGroupProtectionMode(ID=secGrpID, protectionMode=protectionMode, outAsJson=True)

	def setCloudSecurityGroupsProtectionModeOfVpc(self, vpcID, protectionMode):
		vpcSecGrp = self.getCloudSecurityGroupIDsOfVpc(vpcID=vpcID)
		if not vpcSecGrp:
			raise ValueError('got 0 security groups!')
		for secGrpID in vpcSecGrp:
			self.setCloudSecurityGroupProtectionMode(ID=secGrpID, protectionMode=protectionMode, outAsJson=True)

	def updateOrganizationalUnitForCloudAccount(self, vendor, cloudAccountID, organizationalUnitID):
		if vendor == 'aws':
			self.updateOrganizationalUnitForAWSCloudAccount(cloudAccountID, organizationalUnitID)
		elif vendor == 'azure':
			self.updateOrganizationalUnitForAzureCloudAccount(cloudAccountID, organizationalUnitID)

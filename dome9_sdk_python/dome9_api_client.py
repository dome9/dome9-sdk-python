#!/usr/bin/env python

from typing import Union, Optional, Set

from .dome9_api_sdk import Dome9APISDK
from .dome9_api_consts import Regions, ProtectionModes, NewGroupBehaviors, Vendors


class Dome9APIClient(Dome9APISDK):

	def getCloudSecurityGroupsInRegion(self, region: Regions, names: bool = False) -> Set[Union[str, int]]:
		"""Get all security groups in region.

		Args:
			region (Regions): The region.
			names (bool, optional): Should the group names be returned instead of ids. Defaults to False.

		Returns:
			Security groups.

		Raises:
			Dome9APIException: API command failed.
		"""

		groupId = 'name' if names else 'id'

		return {securityGroup[groupId] for securityGroup in self.getAwsSecurityGroups() if securityGroup['regionId'] == region.value}

	def getCloudSecurityGroupsOfVPC(self, vpcId: str, names: bool = False) -> Set[Union[str, int]]:
		"""Get all security groups of VPC.

		Args:
			vpcId (str): The VPC.
			names (bool, optional): Should the group names be returned instead of ids. Defaults to False.

		Returns:
			Security groups.

		Raises:
			Dome9APIException: API command failed.
		"""

		# validate vpcId

		groupId = 'name' if names else 'id'

		return {securityGroup[groupId] for securityGroup in self.getAwsSecurityGroups() if securityGroup['vpcId'] == vpcId}

	def getCloudSecurityGroupsOfAccount(self, accountId: int) -> Set[str]:
		"""Get all security groups of account.

		Args:
			accountId (int):

		Returns:
			Security groups.

		Raises:
			ValueError: Invalid input.
			Dome9APIException: API command failed.
		"""

		Dome9APISDK._checkIsNotNegative(accountId)

		return {securityGroup['externalId'] for securityGroup in self.getAwsSecurityGroups() if securityGroup['awsAccountId'] == accountId}

	def setCloudRegionsProtectedMode(self, cloudAccountId: str, newGroupBehavior: NewGroupBehaviors, regions: Optional[Set[Regions]] = None) -> None:
		"""Update AWS cloud account region configurations.

		Args:
			cloudAccountId (str): Dome9 AWS account id (UUID) or the AWS external account number (12 digit number).
			newGroupBehavior (NewGroupBehaviors): The Protection Mode that Dome9 will apply to new security groups detected in the cloud account. ReadOnly New Security Groups will be included in Dome9 in Read-Only mode, without changes to any of the rules. FullManage New Security Groups will be included in Dome9 in Full Protection mode, without changes to any of the rules. Reset New Security Groups will be included in Dome9 in Full Protection mode, and all inbound and outbound rules will be cleared
			regions (Regions, optional): Dome9 representation value for the AWS region. Defaults to None.

		Raises:
			Dome9APIException: API command failed.
		"""

		# validate cloudAccountId

		tempAllUserRegions = self.getCloudAccountRegions(cloudAccountId=cloudAccountId)
		regionMap = {region.value: region for region in Regions}
		allUserRegions = {regionMap[region] for region in tempAllUserRegions}
		if regions is None:
			cloudAccountRegions = allUserRegions
		else:
			if not regions.issubset(allUserRegions):
				raise ValueError

			cloudAccountRegions = regions

		route = 'cloudaccounts/region-conf'
		for region in cloudAccountRegions:
			body = {
				'externalAccountNumber': cloudAccountId,
				'data'                 : {
					'region'          : region.value,
					'newGroupBehavior': newGroupBehavior.value
				}
			}
			self._request(method=Dome9APISDK._RequestMethods.PUT, route=route, body=body)

	def setCloudSecurityGroupsProtectionModeInRegion(self, region: Regions, protectionMode: ProtectionModes) -> None:
		"""Change the protection mode for all AWS security groups in region.

		Args:
			region (Regions):
			protectionMode (ProtectionModes):

		Raises:
			Dome9APIException: API command failed.
		"""

		securityGroups = self.getCloudSecurityGroupsInRegion(region=region)
		for securityGroupId in securityGroups:
			self.setCloudSecurityGroupProtectionMode(securityGroupId=securityGroupId, protectionMode=protectionMode)

	def setCloudSecurityGroupsProtectionModeOfVPC(self, vpcId: str, protectionMode: ProtectionModes) -> None:
		"""Change the protection mode for all AWS security groups of VPC.

		Args:
			vpcId (str):
			protectionMode (ProtectionModes):

		Raises:
			Dome9APIException: API command failed.
		"""

		# validate vpcId

		securityGroups = self.getCloudSecurityGroupsOfVPC(vpcId=vpcId)
		for securityGroupId in securityGroups:
			self.setCloudSecurityGroupProtectionMode(securityGroupId=securityGroupId, protectionMode=protectionMode)

	def updateOrganizationalUnitForCloudAccount(self, vendor: Vendors, cloudAccountId: str, organizationalUnitId: Optional[str] = None) -> None:
		"""Update the ID of the Organizational unit that this cloud account will be attached to. Use 'null' for root organizational unit.

		Args:
			vendor (Vendors): The vendor.
			cloudAccountId (str): Guid ID of the cloud account.
			organizationalUnitId (str): Guid ID of the Organizational Unit to attach to. Use null in order to attach to root Organizational Unit. Defaults to None.

		Raises:
			ValueError: Invalid input.
			Dome9APIException: API command failed.
		"""

		Dome9APIClient._checkIsUUID(cloudAccountId)
		Dome9APIClient._checkIsUUID(organizationalUnitId)

		if vendor == Vendors.AWS:
			self.updateOrganizationalUnitForAWSCloudAccount(cloudAccountId, organizationalUnitId)
		elif vendor == Vendors.AZURE:
			self.updateOrganizationalUnitForAzureCloudAccount(cloudAccountId, organizationalUnitId)
		else:
			raise NotImplementedError

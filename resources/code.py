from typing import Any, List, Dict, Set, Optional

from dome9 import OperationModes
from dome9.client import Client
from dome9.statics import Statics


def getAllUsers(self) -> List[Any]:
	"""Get all Dome9 users.

	Returns:
		List of Dome9 users.

	Raises:
		Dome9APIException: API command failed.
	"""

	route = 'user'

	return self._request(method=Client.RequestMethods.GET, route=route)


def getCloudAccounts(self) -> Dict[str, Any]:
	"""Get all AWS cloud accounts.

	Returns:
		List of AWS cloud accounts.

	Raises:
		Dome9APIException: API command failed.
	"""

	route = 'CloudAccounts'

	return self._request(method=Client.RequestMethods.GET, route=route)


def getCloudAccountId(self, cloudAccountId: str) -> Dict[str, Any]:
	"""Fetch a specific AWS cloud account.

	Args:
		cloudAccountId (str): Dome9 AWS account id (UUID) or the AWS external account number (12 digit number)

	Returns:
		AWS cloud account.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics._checkIsUUIDOr12Digits(cloudAccountId)

	route = 'CloudAccounts/{}'.format(cloudAccountId)

	return self._request(method=Client.RequestMethods.GET, route=route)


def getCloudAccountRegions(self, cloudAccountId: str) -> Set[str]:
	"""Get all regions used in cloud account.

	Args:
		cloudAccountId (str): Dome9 AWS account id (UUID) or the AWS external account number (12 digit number).

	Returns:
		List of regions.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics._checkIsUUIDOr12Digits(cloudAccountId)

	cloudAccountId = self.getCloudAccountId(cloudAccountId=cloudAccountId)

	return {region['region'] for region in cloudAccountId['netSec']['regions']}


def getRoles(self) -> List[Any]:
	"""Get all roles.

	Returns:
		List of roles.

	Raises:
		Dome9APIException: API command failed.
	"""

	route = 'role'

	return self._request(method=Client.RequestMethods.GET, route=route)


def onBoardingAwsAccount(self,
	arn: str,
	secret: str,
	fullProtection: bool = False,
	allowReadOnly: bool = False,
	name: Optional[str] = None) -> None:
	"""Add a new AWS cloud account to Dome9. Onboarding an AWS cloud account requires granting Dome9 permissions to access the account. The following document describes the required procedure: https://helpcenter.dome9.com/hc/en-us/articles/360003994613-Onboard-an-AWS-Account

	Args:
		arn (str): AWS Role ARN (to be assumed by Dome9 System)
		secret (str): AWS role External ID (Dome9 System will have to use this secret in order to assume the role)
		fullProtection (bool): As part of the AWS account onboarding, the account security groups are imported. This flag determines whether to enable Tamper Protection mode for those security groups. Defaults to False.
		allowReadOnly (bool): Determines the AWS cloud account operation mode. For "Manage" set to true, for "Readonly" set to false. Defaults to False.
		name (str, optional): Cloud account name. Defaults to None.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics._checkIsARN(arn)
	Statics.checkOnlyContainsLowercaseAlphanumeric(secret)

	route = 'CloudAccounts'
	body = {
		'name': name,
		'credentials': {
		'arn': arn,
		'secret': secret,
		'type': 'RoleBased'
		},
		'fullProtection': fullProtection,
		'allowReadOnly': allowReadOnly
	}
	self._request(method=Client.RequestMethods.POST, route=route, body=body)


def onBoardingAzureAccount(self,
	subscriptionId: str,
	tenantId: str,
	clientId: str,
	clientPassword: str,
	name: Optional[str] = None,
	operationMode: OperationModes = OperationModes.READ) -> None:
	"""Add (onboard) an Azure account to the user's Dome9 account.

	Args:
		subscriptionId (str): Azure subscription id for account.
		tenantId (str): Azure tenant id.
		clientId (str): Azure account id.
		clientPassword (str): Password for account.
		name (str, optional): Account name (in Dome9). Defaults to None.
		operationMode (OperationModes): Dome9 operation mode for the Azure account (Read or Managed). Defaults to Read.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics.checkIsUUID(subscriptionId)
	Statics.checkIsUUID(tenantId)
	Statics.checkIsUUID(clientId)

	route = 'AzureCloudAccount'
	body = {
		'name': name,
		'subscriptionId': subscriptionId,
		'tenantId': tenantId,
		'credentials': {
		'clientId': clientId,
		'clientPassword': clientPassword
		},
		'operationMode': operationMode.value,
	}
	self._request(method=Client.RequestMethods.POST, route=route, body=body)


def updateAwsAccountCredentials(self,
	arn: str,
	secret: str,
	externalAccountNumber: Optional[str] = None,
	cloudAccountId: Optional[str] = None) -> None:
	"""Update credentials for an AWS cloud account in Dome9. At least one of the following properties must be provided: "cloudAccountId", "externalAccountNumber".

	Args:
		arn (str): AWS Role ARN (to be assumed by Dome9 System).
		secret (str): The AWS role External ID (Dome9 System will have to use this secret in order to assume the role).
		externalAccountNumber (str, optional): Aws external account number, at least one of the following properties must be provided: "cloudAccountId", "externalAccountNumber". Defaults to None.
		cloudAccountId (str, optional): The Dome9 cloud account id, at least one of the following properties must be provided: "cloudAccountId", "externalAccountNumber". Defaults to None.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics._checkIsARN(arn)
	Statics.checkOnlyContainsLowercaseAlphanumeric(secret)
	# check externalAccountNumber format
	Statics.checkIsUUID(cloudAccountId, optional=True)

	route = 'CloudAccounts/credentials'
	body = {
		'cloudAccountId': cloudAccountId,
		'externalAccountNumber': externalAccountNumber,
		'data': {
		'arn': arn,
		'secret': secret,
		'type': 'RoleBased'
		}
	}
	self._request(method=Client.RequestMethods.PUT, route=route, body=body)


def updateOrganizationalUnitForAWSCloudAccount(self, cloudAccountId: str, organizationalUnitId: Optional[str] = None) -> Dict[str, Any]:
	"""Update the ID of the Organizational unit that this cloud account will be attached to. Use 'null' for root organizational unit.

	Args:
		cloudAccountId (str): Guid ID of the AWS cloud account.
		organizationalUnitId (str, optional): Guid ID of the Organizational Unit to attach to. Use null in order to attach to root Organizational Unit. Defaults to None.

	Returns:
		Cloud account.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics.checkIsUUID(cloudAccountId)
	Statics.checkIsUUID(organizationalUnitId, optional=True)

	route = 'cloudaccounts/{}/organizationalUnit'.format(cloudAccountId)
	body = {'organizationalUnitId': organizationalUnitId}

	return self._request(method=Client.RequestMethods.PUT, route=route, body=body)


def updateOrganizationalUnitForAzureCloudAccount(self, cloudAccountId: str, organizationalUnitId: Optional[str] = None) -> Dict[str, Any]:
	"""Update the ID of the Organizational unit that this cloud account will be attached to. Use 'null' for root organizational unit.

	Args:
		cloudAccountId (str): Guid ID of the Azure cloud account.
		organizationalUnitId (str, optional): Guid ID of the Organizational Unit to attach to. Use null in order to attach to root Organizational Unit. Defaults to None.

	Returns:
		Azure cloud account.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics.checkIsUUID(cloudAccountId)
	Statics.checkIsUUID(organizationalUnitId, optional=True)

	route = 'AzureCloudAccount/{}/organizationalUnit'.format(cloudAccountId)
	body = {'organizationalUnitId': organizationalUnitId}

	return self._request(method=Client.RequestMethods.PUT, route=route, body=body)


def updateRoleById(self,
	roleId: int,
	roleName: str,
	access: Optional[List[str]] = None,
	manage: Optional[List[str]] = None,
	create: Optional[List[str]] = None,
	view: Optional[List[str]] = None,
	crossAccountAccess: Optional[List[str]] = None) -> None:
	"""Update a role.

	Args:
		roleId (int): Role id.
		roleName (str): Role Name.
		access (List[str], optional): Access permission list (list of SRL). Defaults to None.
		manage (List[str], optional): Manage permission list (list of SRL). Defaults to None.
		create (List[str], optional): Create permission list (list of SRL). Defaults to None.
		view (List[str], optional): View permission list (list of SRL). Defaults to None.
		crossAccountAccess (List[str], optional): -. Defaults to None.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics._checkIsNotNegative(roleId)
	Statics._checkIsNotEmpty(roleName)

	body = {
		'name': roleName,
		'permissions': {
		'access': access,
		'manage': manage,
		'create': create,
		'view': view,
		'crossAccountAccess': crossAccountAccess
		}
	}
	route = 'Role/{}'.format(roleId)
	self._request(method=Client.RequestMethods.PUT, route=route, body=body)


def getRoleById(self, roleId: int) -> Dict[str, Any]:
	"""Get the specific role with the specified id.

	Args:
		roleId (int): Role id.

	Returns:
		Role.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics._checkIsNotNegative(roleId)

	route = 'Role/{}'.format(roleId)

	return self._request(method=Client.RequestMethods.GET, route=route)


# doesn't exist in documentation
def updateCloudAccountID(self,
	cloudAccountId: str,
	name: Optional[str] = None,
	fullProtection: Optional[bool] = None,
	allowReadOnly: Optional[bool] = None,
	organizationalUnitId: Optional[str] = None,
	organizationalUnitPath: Optional[str] = None,
	organizationalUnitName: Optional[str] = None,
	lambdaScanner: Optional[bool] = None,
	arn: Optional[str] = None,
	secret: Optional[str] = None) -> None:
	"""Edit an existing AWS cloud account on Dome9.

	Args:
		cloudAccountId (str): Dome9 id.
		name (str, optional): Cloud account name. Defaults to None.
		fullProtection (bool, optional): As part of the AWS account onboarding, the account security groups are imported. This flag determines whether to enable Tamper Protection mode for those security groups. Defaults to None.
		allowReadOnly (bool, optional): Determines the AWS cloud account operation mode. For "Manage" set to true, for "Readonly" set to false. Defaults to None.
		organizationalUnitId (str, optional): -. Defaults to None.
		organizationalUnitPath (str, optional): -. Defaults to None.
		organizationalUnitName (str, optional): -. Defaults to None.
		lambdaScanner (bool, optional): Flag indicating if lambda scanner is enabled/disabled for the account. Defaults to None.
		arn (str, optional): AWS Role ARN (to be assumed by Dome9 System). Defaults to None.
		secret (str, optional): AWS role External ID (Dome9 System will have to use this secret in order to assume the role). Defaults to None.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics.checkIsUUID(cloudAccountId)
	Statics.checkIsUUID(organizationalUnitId, optional=True)
	# validate organizationalUnitPath
	# validate organizationalUnitName
	Statics._checkIsARN(arn)
	Statics.checkOnlyContainsLowercaseAlphanumeric(secret)

	route = 'CloudAccounts/{}'.format(cloudAccountId)
	body = {
		'name': name,
		'fullProtection': fullProtection,
		'allowReadOnly': allowReadOnly,
		'organizationalUnitId': organizationalUnitId,
		'organizationalUnitPath': organizationalUnitPath,
		'organizationalUnitName': organizationalUnitName,
		'lambdaScanner': lambdaScanner,
		'CloudAccountCredentials': {
		'arn': arn,
		'secret': secret,
		'type': 'RoleBased'
		}
	}
	self._request(method=Client.RequestMethods.PATCH, route=route, body=body)


def getCloudTrail(self) -> List[Any]:
	"""Get CloudTrail events for a Dome9 user.

	Returns:
		List of CloudTrail events.

	Raises:
		Dome9APIException: API command failed.
	"""

	route = 'CloudTrail'

	return self._request(method=Client.RequestMethods.GET, route=route)


def getFlatOrganizationalUnits(self) -> List[Any]:
	"""Get all organizational units flat.

	Returns:
		List of flat organizational units.

	Raises:
		Dome9APIException: API command failed.
	"""

	route = 'organizationalunit/GetFlatOrganizationalUnits'

	return self._request(method=Client.RequestMethods.GET, route=route)


# doesn't exist in documentation
def getAwsSecurityGroups(self):
	"""Get all security groups.

	Returns:
		Security groups.

	Raises:
		Dome9APIException: API command failed.
	"""

	return self._request(method=Client.RequestMethods.GET, route='view/awssecuritygroup/index')


def getCloudSecurityGroup(self, cloudAccountId: str, regionId: Regions) -> List[Any]:
	"""Get AWS security groups for a specific cloud account and region.

	Args:
		cloudAccountId (str): Cloud account id.
		regionId (Regions): Region.

	Returns:
		List of security groups.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics.checkIsUUID(cloudAccountId)

	route = 'cloudsecuritygroup/{}'.format(cloudAccountId)
	params = {'cloudAccountId': cloudAccountId, 'regionId': regionId.value}

	return self._request(method=Client.RequestMethods.GET, route=route, params=params)


def getAllEntityFetchStatus(self, cloudAccountId: str) -> List[Any]:
	"""This EntityFetchStatus resource queries the status of system data fetching by Dome9. Dome9 fetches information from cloud accounts and occasionally needs to refresh this information (typically in DevSecOps pipeline scenarios). This resource is used together with the SyncNow method in the CloudAccounts resource to fetch fresh cloud account data.

	Args:
		cloudAccountId (str): Dome9 CloudAccountId which can replace the AWS externalAccountNumber.

	Returns:
		List of fetcher run statuses.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics.checkIsUUID(cloudAccountId)

	route = 'EntityFetchStatus'
	params = {'cloudAccountId': cloudAccountId}

	return self._request(method=Client.RequestMethods.GET, route=route, params=params)


def cloudAccountSyncNow(self, cloudAccountId: str) -> Dict[str, Any]:
	"""Send a data sync command to immediately fetch cloud account data into Dome9's system caches. This API is used in conjunction with EntityFetchStatus API resource to query the fetch status. Read more and see a full example here: https://github.com/Dome9/Python_API_SDK/blob/master/implementation/runSyncAssessment.md

	Args:
		cloudAccountId (str): Account id.

	Returns:
		AWS sync now result.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics.checkIsUUID(cloudAccountId)

	route = 'cloudaccounts/{}/SyncNow'.format(cloudAccountId)

	return self._request(method=Client.RequestMethods.POST, route=route)


def setCloudSecurityGroupProtectionMode(self, securityGroupId: str, protectionMode: ProtectionModes) -> None:
	"""Change the protection mode for an AWS security group.

	Args:
		securityGroupId (str): AWS security group id (Dome9 internal ID / AWS security group ID).
		protectionMode (ProtectionModes): Details for the security group, including the protection mode. Only 'ProtectionMode' is required in this call (FullManage or ReadOnly).

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	# validate securityGroupId

	route = 'cloudsecuritygroup/{}/protection-mode'.format(securityGroupId)
	body = {'protectionMode': protectionMode}
	self._request(method=Client.RequestMethods.POST, route=route, body=body)


def runAssessmentBundle(self, bundleId: int, cloudAccountId: str, cloudAccountType: CloudAccountTypes, name: Optional[str],
	description: Optional[str], isCft: Optional[bool], dome9CloudAccountId: Optional[str],
	externalCloudAccountId: Optional[str], region: Optional[Regions], cloudNetwork: Optional[str],
	rootName: Optional[str], params: Optional[List[Dict]], files: Optional[List[Dict]]) -> Dict[str, Any]:
	"""Run an assessment on a cloud environment using a bundle (V2).

	Args:
		bundleId (int): Bundle id.
		cloudAccountId (str): Account id on cloud provider (AWS, Azure, GCP).
		cloudAccountType (CloudAccountTypes): Cloud provider (AWS/Azure/GCP).
		name (str, optional): Bundle name. Defaults to None.
		description (str, optional): Bundle description. Defaults to None.
		isCft (bool, optional): Indicates request target is a CFT (template file). Defaults to None.
		dome9CloudAccountId (str, optional): Dome9 account id. Defaults to None.
		externalCloudAccountId (str, optional): Account id on cloud provider (AWS, Azure, GCP). Defaults to None.
		region (Regions, optional): Cloud region for the account. Defaults to None.
		cloudNetwork (str, optional): Cloud provider (AWS/Azure/GCP). Defaults to None.
		rootName (str, optional): -. Defaults to None.
		params (List[Dict], optional): -. Defaults to None.
		files (List[Dict], optional): -. Defaults to None.

	Returns:
		Assessment result (aggregates results from multiple tests).

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics._checkIsNotNegative(bundleId)
	# validate cloudAccountId
	# validate dome9CloudAccountId
	# validate externalCloudAccountId
	# validate cloudNetwork
	# validate rootName
	# validate params
	# validate files

	route = 'assessment/bundleV2'
	body = {
		'id': bundleId,
		'cloudAccountId': cloudAccountId,
		'cloudAccountType': cloudAccountType.value,
		'name': name,
		'description': description,
		'isCft': isCft,
		'dome9CloudAccountId': dome9CloudAccountId,
		'externalCloudAccountId': externalCloudAccountId,
		'region': region.value,
		'cloudNetwork': cloudNetwork,
		'cft': {
		'rootName': rootName,
		'params': params,
		'files': files
		}
	}

	return self._request(method=Client.RequestMethods.POST, route=route, body=body)


def getAccountBundles(self) -> List[Any]:
	"""Get all bundles.

	Returns:
		List of rule bundle results.

	Raises:
		Dome9APIException: API command failed.
	"""

	route = 'CompliancePolicy'

	return self._request(method=Client.RequestMethods.GET, route=route)


def updateRuleBundleById(self, bundleId: int, rules: List[Dict[str, Any]]) -> Dict[str, Any]:
	"""Update a Bundle.

	Args:
		bundleId (int): Bundle id.
		rules (List[Dict[str, Any]]): List of rules in the bundle.

	Return:
		Rule bundle result.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics._checkIsNotNegative(bundleId)
	# validate rules

	route = 'CompliancePolicy'
	body = {'id': bundleId, 'rules': rules}

	return self._request(method=Client.RequestMethods.PUT, route=route, body=body)


def acquireAwsLease(self,
	cloudAccountId: str,
	securityGroupId: int,
	ip: str,
	portFrom: int,
	portTo: Optional[int] = None,
	protocol: Optional[Protocols] = None,
	duration: Optional[str] = None,
	region: Optional[Regions] = None,
	accountId: Optional[int] = None,
	name: Optional[str] = None,
	user: Optional[str] = None) -> None:
	"""Acquires an AWS lease.

	Args:
		cloudAccountId (str): AWS account id.
		securityGroupId (int): Security Group affected by lease.
		ip (str): IP address that will be granted elevated access.
		portFrom (int): Lowest IP port in range for the lease.
		portTo (int, optional): Highest IP port in range for the lease. Defaults to None.
		protocol (Protocols, optional): Network protocol to be used in the lease. Defaults to None.
		duration (str, optional): Duration of the lease ([D].H:M:S). Defaults to None.
		region (Regions, optional): AWS region. Defaults to None.
		accountId (int, optional): Account id. Defaults to None.
		name (str, optional): Defaults to None.
		user (str, optional): User for whom the lease was created. Defaults to None.

	Raises:
		ValueError: Invalid input.
		Dome9APIException: API command failed.
	"""

	Statics.checkIsUUID(cloudAccountId)
	Statics._checkIsNotNegative(securityGroupId)  # doc says is string
	Statics._checkIsIP(ip)
	Statics._checkIsPort(portFrom)
	Statics._checkIsPort(portTo, optional=True)
	Statics._checkIsDuration(duration, optional=True)
	Statics._checkIsNotNegative(accountId, optional=True)
	Statics._checkIsEmail(user, optional=True)

	route = 'accesslease/aws'
	body = {
		'cloudAccountId': cloudAccountId,
		'securityGroupId': securityGroupId,
		'ip': ip,
		'portFrom': portFrom,
		'portTo': portTo,
		'protocol': protocol,
		'length': duration,
		'region': region,
		'accountId': accountId,
		'name': name,
		'user': user
	}
	self._request(method=Client.RequestMethods.POST, route=route, body=body)

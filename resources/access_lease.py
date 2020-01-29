from dataclasses import dataclass
from enum import Enum
from typing import Dict

from loguru import logger

from dome9 import Dome9Resource, Client, APIUtils, BaseDataclassRequest


class AccessLeaseConsts(Enum):
	ACCESS_LEASE = 'accessLease'
	AWS_CLOUD_ACCOUNT = 'aws'


@dataclass
class AccessLeaseRequest(BaseDataclassRequest):
	"""Restricted iam entities request

	:link  https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-models-awsaccessleasepostviewmodel
	:param cloud_account_id: Cloud account id
	:type  cloud_account_id: str
	:param region: Aws region
	:type  region: str
	:param security_group_id: Security group id
	:type  security_group_id: str
	:param protocol: Protocol type
	:type  protocol: str
	:param port_from: From port
	:type  port_from: str
	:param port_to: To port
	:type  port_to: str

	"""
	cloud_account_id: str
	region: str
	security_group_id: str
	protocol: str
	port_from: str = None
	port_to: str = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		APIUtils.check_is_valid_aws_region_id(self.region)
		APIUtils.check_is_valid_protocol(self.protocol)


class AccessLease(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client=client)

	def active_lease(self, body: AccessLeaseRequest) -> Dict:
		"""Active lease access lease

		:link   https://api-v2-docs.dome9.com/index.html?python#accesslease_acquireawslease
		:param  body: Details for the access lease
		:type   body: AccessLeaseRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-models-awsaccessleasepostviewmodel
		:rtype  AwsAccessLeasePost

		"""
		route = f'{AccessLeaseConsts.ACCESS_LEASE.value}/{AccessLeaseConsts.AWS_CLOUD_ACCOUNT.value}'
		return self._post(route=route, body=body)

	def get_all(self) -> Dict:
		"""Get information for all the activated leases

		:link   https://api-v2-docs.dome9.com/index.html?python#accesslease_get
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-models-accessleasesgroupedviewmodel
		:rtype  AccessLeasesGrouped

		"""
		return self._get(route=AccessLeaseConsts.ACCESS_LEASE.value)

	def terminate_lease(self, lease_id: str) -> None:
		"""Terminate lease

		:link https://api-v2-docs.dome9.com/index.html?python#accesslease_delete
		:param lease_id: Lease id
		:type lease_id: str

		"""
		route = f'{AccessLeaseConsts.ACCESS_LEASE.value}/{lease_id}'
		return self._delete(route=route)

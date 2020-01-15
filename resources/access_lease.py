from dataclasses import dataclass
from enum import Enum
from typing import Dict

from loguru import logger

from dome9 import Dome9Resource, Client, APIUtils, BaseDataclassRequest


class AccessLeaseConsts(Enum):
	MAIN_ROUTE = 'accessLease'
	AWS_CLOUD_ACCOUNT = 'aws'


@dataclass
class AccessLeaseRequest(BaseDataclassRequest):
	"""Restricted iam entities request

		Args:
			cloud_account_id (str): Cloud account id
			region (str): Aws region
			security_group_id (str): Security group id
			protocol (str): Protocol type
			port_from (str): From port
			port_to (str): To port

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

		:param body: Details for the access lease
		:type body: AccessLeaseRequest
		:returns: Dict that has metadata for the activated lease

		"""
		route = f'{AccessLeaseConsts.MAIN_ROUTE.value}/{AccessLeaseConsts.AWS_CLOUD_ACCOUNT.value}'
		return self._post(route=route, body=body)

	def get_all(self) -> Dict:
		"""Get information for all the activated leases

		:returns: Dict that has metadata for all the activated leases

		"""
		return self._get(route=AccessLeaseConsts.MAIN_ROUTE.value)

	def terminate_lease(self, lease_id: str) -> None:
		"""Terminate lease

		:param lease_id: Lease id
		:type lease_id: str
		:returns: None

		"""
		route = f'{AccessLeaseConsts.MAIN_ROUTE.value}/{lease_id}'
		return self._delete(route=route)

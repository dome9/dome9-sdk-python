from typing import Dict

from resources.access_lease import AccessLease as BaseAccessLease, AccessLeaseRequest


class access_lease(BaseAccessLease):

	@classmethod
	def active_lease(cls, body: AccessLeaseRequest) -> Dict:
		"""Active lease access lease

		:link   https://api-v2-docs.dome9.com/index.html?python#accesslease_acquireawslease
		:param  body: Details for the access lease
		:type   body: AccessLeaseRequest
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-models-awsaccessleasepostviewmodel
		:rtype  AwsAccessLeasePost

		"""
		pass

	@classmethod
	def get_all(cls) -> Dict:
		"""Get information for all the activated leases

		:link   https://api-v2-docs.dome9.com/index.html?python#accesslease_get
		:return https://api-v2-docs.dome9.com/index.html?python#schemadome9-web-api-models-accessleasesgroupedviewmodel
		:rtype  AccessLeasesGrouped

		"""
		pass

	@classmethod
	def terminate_lease(cls, lease_id: str) -> None:
		"""Terminate lease

		:link https://api-v2-docs.dome9.com/index.html?python#accesslease_delete
		:param lease_id: Lease id
		:type lease_id: str

		"""
		pass

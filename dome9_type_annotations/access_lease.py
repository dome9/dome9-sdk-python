from typing import Dict

from resources.access_lease import AccessLeaseRequest
from resources.access_lease import AccessLease as BaseAwsCloudAccount


class access_lease(BaseAwsCloudAccount):

	@classmethod
	def active_lease(cls, body: AccessLeaseRequest) -> Dict:
		pass

	@classmethod
	def get_all(cls) -> Dict:
		pass

	@classmethod
	def terminate_lease(cls, lease_id: str) -> None:
		pass

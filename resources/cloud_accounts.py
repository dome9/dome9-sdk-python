from typing import Any, Dict

from dome9.client import Client


class CloudAccounts(Client):

	def getCloudAccounts(self) -> Dict[str, Any]:
		"""Get all AWS cloud accounts.

		Returns:
			List of AWS cloud accounts.

		Raises:
			Dome9APIException: API command failed.
		"""

		route = 'CloudAccounts'

		return self._request(method=Client.RequestMethods.GET, route=route)

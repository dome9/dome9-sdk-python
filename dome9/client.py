import requests
from enum import Enum
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth
from typing import Dict, Any, Union, Optional, List, Set

from .exceptions import Dome9APIException
from .consts import Protocols, Regions, OperationModes, ProtectionModes, CloudAccountTypes
from .statics import Statics


class Client:

	class _RequestMethods(Enum):
		GET = 'get'
		POST = 'post'
		PATCH = 'patch'
		PUT = 'put'
		DELETE = 'delete'

	_ORIGIN = 'https://api.dome9.com/v2/'

	def __init__(self, key: str, secret: str, origin: str = _ORIGIN):
		"""Initializes a Dome9 API SDK object.

		Args:
			key (str): API id (key).
			secret (str): API secret.
			origin (str): Origin of API (URL). Defaults to 'https://api.dome9.com/v2/'.
		"""

		Statics._checkIsUUID(key)
		Statics._checkOnlyContainsLowercaseAlphanumeric(secret)
		Statics._checkIsHTTPURL(origin)

		self._origin = origin
		self._clientAuth = HTTPBasicAuth(key, secret)

	def _request(self, method: _RequestMethods, route: str, body: Any = None, params: Optional[Dict[str, Union[str, int]]] = None) -> Any:
		url = urljoin(self._origin, route)
		headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
		try:
			response = getattr(requests, method.value)(url=url, json=body, params=params, headers=headers, auth=self._clientAuth)
		except requests.ConnectionError as connectionError:
			raise Dome9APIException('{} {}'.format(url, str(connectionError)))

		if response.status_code not in range(200, 299):
			raise Dome9APIException(message=response.reason, code=response.status_code, content=response.content)

		if response.content:
			try:
				jsonResponse = response.json()

				return jsonResponse

			except ValueError as valueError:
				raise Dome9APIException(message=str(valueError), code=response.status_code, content=response.content)

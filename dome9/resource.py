from typing import Optional, Dict, Union, Any
from urllib.parse import urljoin

import requests
from loguru import logger

from dome9.exceptions import Dome9APIException
from dome9.client import Client
from dome9.consts import RequestMethods, SuccessCodes
from dome9.logger import LoggerController


class Dome9Resource:

	def __init__(self, client: Client):
		"""dome9 base resources class

		Args:
			client (Client): D9 client
		"""
		self._client = client
		self.logger_controller = LoggerController(config=client._config)

	# crud methods
	def _get(self, route: str, body=None):
		return self.__request(method=RequestMethods.GET.value, route=route, body=body)

	def _post(self, route: str, body=None):
		return self.__request(method=RequestMethods.POST.value, route=route, body=body)

	def _patch(self, route: str, body=None):
		return self.__request(method=RequestMethods.PATCH.value, route=route, body=body)

	def _put(self, route: str, body=None):
		return self.__request(method=RequestMethods.PUT.value, route=route, body=body)

	def _delete(self, route: str, body=None):
		return self.__request(method=RequestMethods.DELETE.value, route=route, body=body)

	@logger.catch(reraise=True)
	def __request(self, method: str, route: str, body: Any = None, params: Optional[Dict[str, Union[str, int]]] = None) -> Any:
		url = urljoin(self._client._config.base_url, route)
		body = body if not body else body.load()
		try:
			logger.debug(f'performing request: {method}, url: {url}, params: {params}, body: {body}')
			response = getattr(requests, method)(url=url,
				json=body,
				params=params,
				headers=self._client._config.headers,
				auth=self._client._config.client_auth)
		except requests.ConnectionError as connectionError:
			raise Dome9APIException(f'{url} {connectionError}')

		logger.debug(f'response received: {response}')

		if response.status_code not in range(SuccessCodes.MIN.value, SuccessCodes.MAX.value):
			exception = Dome9APIException(message=response.reason, code=response.status_code, content=response.content)
			logger.exception(exception)
			raise exception

		if response.content:
			try:
				json_response = response.json()

				return json_response

			except ValueError as valueError:
				exception = Dome9APIException(message=str(valueError), code=response.status_code, content=response.content)
				logger.exception(exception)
				raise exception

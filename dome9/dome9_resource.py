from typing import Optional, Dict, Union, Any
from urllib.parse import urljoin

import requests
from loguru import logger

from dome9 import Dome9APIException
from dome9.client import Client
from dome9.consts import RequestMethods
from dome9.logger import LoggerController


class Dome9Resource:

	def __init__(self, client: Client):
		"""dome9 base resources class

		Args:
			client (Client): D9 client
		"""
		self._client = client
		self.loggerController = LoggerController(config=self._client._config)

	# crud methods
	def get(self, route: str, body=None):
		return self.__request(method=RequestMethods.GET, route=route, body=body)

	def post(self, route: str, body=None):
		return self.__request(method=RequestMethods.POST, route=route, body=body)

	def patch(self, route: str, body=None):
		return self.__request(method=RequestMethods.PATCH, route=route, body=body)

	def put(self, route: str, body=None):
		return self.__request(method=RequestMethods.PUT, route=route, body=body)

	def delete(self, route: str, body=None):
		return self.__request(method=RequestMethods.DELETE, route=route, body=body)

	@logger.catch
	def __request(self, method: str, route: str, body: Any = None, params: Optional[Dict[str, Union[str, int]]] = None) -> Any:
		url = urljoin(self._client._config.baseURL, route)

		try:
			logger.debug(f'performing request: {method}, url: {url}, params: {params}, body: {body}')
			response = getattr(requests, method)(url=url,
				json=body,
				params=params,
				headers=self._client._config.headers,
				auth=self._client._config.clientAuth)
		except requests.ConnectionError as connectionError:
			raise Dome9APIException(f'{url} {connectionError}')

		logger.debug(f'response received: {response}')

		if response.status_code not in range(200, 299):
			raise Dome9APIException(message=response.reason, code=response.status_code, content=response.content)

		if response.content:
			try:
				jsonResponse = response.json()

				return jsonResponse

			except ValueError as valueError:
				raise Dome9APIException(message=str(valueError), code=response.status_code, content=response.content)

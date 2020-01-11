from functools import lru_cache
from importlib import import_module
from os import listdir, getenv, path, environ, chdir
from os.path import isfile

from requests.auth import HTTPBasicAuth
from loguru import logger

from dome9.consts import ConfigConsts, LoggerConsts, ClientConsts
from dome9.exceptions import Dome9AccessIDNotFoundException, Dome9SecretKeyNotFoundException

from dome9.statics import Statics


class Client:

	@lru_cache()
	def __new__(cls, **kwargs):
		return super().__new__(cls)

	# prevent to update client's attributes (resources)
	def __setattr__(self, name, value):
		if hasattr(self, name):
			raise Exception(f'can not update client attributes {name}')

		super().__setattr__(name, value)

	def __init__(self,
		access_id: str = None,
		secret_key: str = None,
		base_url: str = ConfigConsts.DEFAULT_BASE_URL.value,
		logger_path: str = None,
		logger_level: str = ConfigConsts.DEFAULT_LOG_LEVEL.value,
		logger_rotation: str = ConfigConsts.DEFAULT_LOGGER_ROTATION.value):
		"""initializes a d9 SDK object.

		Args:
			access_id (str): API key.
			secret_key (str): API secret.
			base_url (str): Origin of API (URL). Defaults to 'https://api.dome9.com/v2/'.
		"""
		self._config = Config(access_id=access_id,
			secret_key=secret_key,
			base_url=base_url,
			logger_path=logger_path,
			logger_level=logger_level,
			logger_rotation=logger_rotation)

		# change working directory to root project
		chdir(f'{path.dirname(path.realpath(__file__))}/../')

		# set all resources as client's attributes
		for file in listdir(ClientConsts.RESOURCES.value):
			if file.endswith(ClientConsts.PY_EXTENSION.value) and isfile(f'{ClientConsts.RESOURCES.value}/{file}'):
				module_name, _ = path.splitext(file)
				class_name = ''.join(word.title() for word in module_name.split('_'))
				try:
					class_object = getattr(import_module(f'{ClientConsts.RESOURCES.value}.{module_name}'), class_name)
				except AttributeError as e:
					logger.warning(e)
					continue

				class_instance = class_object(client=self)
				setattr(self, module_name, class_instance)


class Config:

	@logger.catch(reraise=True)
	def __init__(self,
		access_id: str,
		secret_key: str,
		base_url: str = None,
		logger_path: str = None,
		logger_level: str = ConfigConsts.DEFAULT_LOG_LEVEL.value,
		logger_rotation: str = ConfigConsts.DEFAULT_LOGGER_ROTATION.value):
		"""d9 client configuration.

		Args:
			access_id (str): API key.
			secret_key (str): API secret.
			base_url (str): Origin of API (URL)
			logger_level (str): Logger level. Defaults to INFO
			logger_path (str): Logger file path. Defaults to None
			logger_rotation (str): Logger rotation. Defaults to 100 MB
		"""
		if not access_id:
			try:
				access_id = environ[ConfigConsts.DOME9_ACCESS_ID.value]
			except KeyError:
				raise Dome9AccessIDNotFoundException(f'{ConfigConsts.DOME9_ACCESS_ID.value} was not provided')

		if not secret_key:
			try:
				secret_key = environ[ConfigConsts.DOME9_SECRET_KEY.value]
			except KeyError:
				raise Dome9SecretKeyNotFoundException(f'{ConfigConsts.DOME9_SECRET_KEY.value} was not provided')

		Statics.check_is_uuid(arg=access_id)
		Statics.check_only_contains_lowercase_alphanumeric(arg=secret_key)
		Statics.check_is_http_url(arg=base_url)

		self.logger_level = getenv(LoggerConsts.LOG_LEVEL.value, logger_level)
		self.logger_file_path = getenv(LoggerConsts.LOG_FILE_PATH.value, logger_path)
		self.logger_rotation = logger_rotation

		self.headers = {
			ConfigConsts.ACCEPT.value: ConfigConsts.DEFAULT_FORMAT.value,
			ConfigConsts.CONTENT_TYPE.value: ConfigConsts.DEFAULT_FORMAT.value
		}

		self.base_url = base_url if base_url else ConfigConsts.DEFAULT_BASE_URL.value
		self.client_auth = HTTPBasicAuth(username=access_id, password=secret_key)

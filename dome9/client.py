from functools import lru_cache
from importlib import import_module
from os import listdir, getenv, path, environ, chdir
from os.path import isfile

from requests.auth import HTTPBasicAuth
from loguru import logger

from dome9.consts import ConfigConsts, LoggerConsts, ClientConsts
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
		accessID: str = None,
		secretKey: str = None,
		baseURL: str = ConfigConsts.DEFAULT_BASE_URL.value,
		loggerPath: str = None,
		loggerLevel: str = ConfigConsts.DEFAULT_LOG_LEVEL.value,
		loggerRotation: str = ConfigConsts.DEFAULT_LOGGER_ROTATION.value):
		"""initializes a d9 SDK object.

		Args:
			accessID (str): API key.
			secretKey (str): API secret.
			baseURL (str): Origin of API (URL). Defaults to 'https://api.dome9.com/v2/'.
		"""
		self._config = Config(accessID=accessID,
			secretKey=secretKey,
			baseURL=baseURL,
			loggerPath=loggerPath,
			loggerLevel=loggerLevel,
			loggerRotation=loggerRotation)

		# change working directory to root project
		chdir(f'{path.dirname(path.realpath(__file__))}/../')

		# set all resources as client's attributes
		for file in listdir(ClientConsts.RESOURCES.value):
			if file.endswith(ClientConsts.PY_EXTENSION.value) and isfile(f'{ClientConsts.RESOURCES.value}/{file}'):
				moduleName, _ = path.splitext(file)
				className = ''.join(word.title() for word in moduleName.split('_'))
				try:
					classObject = getattr(import_module(f'{ClientConsts.RESOURCES.value}.{moduleName}'), className)
				except AttributeError as e:
					logger.warning(e)
					continue

				classInstance = classObject(client=self)
				setattr(self, moduleName, classInstance)


class Config:

	def __init__(self,
		accessID: str,
		secretKey: str,
		baseURL: str = None,
		loggerPath: str = None,
		loggerLevel: str = ConfigConsts.DEFAULT_LOG_LEVEL.value,
		loggerRotation: str = ConfigConsts.DEFAULT_LOGGER_ROTATION.value):
		"""d9 client configuration.

		Args:
			accessID (str): API key.
			secretKey (str): API secret.
			baseURL (str): Origin of API (URL)
			loggerLevel (str): Logger level. Defaults to INFO
			loggerPath (str): Logger file path. Defaults to None 
			loggerRotation (str): Logger rotation. Defaults to 100 MB
		"""
		if not accessID:
			accessID = environ[ConfigConsts.DOME9_ACCESS_ID.value]

		if not secretKey:
			secretKey = environ[ConfigConsts.DOME9_SECRET_KEY.value]

		Statics.checkIsUUID(arg=accessID)
		Statics.checkOnlyContainsLowercaseAlphanumeric(arg=secretKey)
		Statics.checkIsHTTPURL(arg=baseURL)

		self.loggerLevel = getenv(LoggerConsts.LOG_LEVEL.value, loggerLevel)
		self.loggerFilePath = getenv(LoggerConsts.LOG_FILE_PATH.value, loggerPath)
		self.loggerRotation = loggerRotation

		self.headers = {
			ConfigConsts.ACCEPT.value: ConfigConsts.DEFAULT_FORMAT.value,
			ConfigConsts.CONTENT_TYPE.value: ConfigConsts.DEFAULT_FORMAT.value
		}

		self.baseURL = baseURL if baseURL else ConfigConsts.DEFAULT_BASE_URL.value
		self.clientAuth = HTTPBasicAuth(username=accessID, password=secretKey)

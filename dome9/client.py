from functools import lru_cache
from importlib import import_module
from os import listdir, getenv, path, environ
from os.path import isfile

from requests.auth import HTTPBasicAuth
from loguru import logger

from dome9.consts import ConfigConsts, LoggerConsts

from dome9.statics import Statics


class Client:

	@lru_cache()
	def __new__(cls, **kwargs):
		return super().__new__(cls)

	def __init__(self,
		accessID: str = None,
		secretKey: str = None,
		baseURL: str = ConfigConsts.DEFAULT_BASE_URL,
		loggerPath: str = None,
		loggerLevel: str = ConfigConsts.DEFAULT_LOG_LEVEL,
		loggerRotation: str = ConfigConsts.DEFAULT_LOGGER_ROTATION):
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

		# set all resources as client's attributes
		for file in listdir('resources'):
			if file.endswith('.py') and isfile(f'resources/{file}'):
				# TODO: OS Basename
				moduleName = path.splitext(file)[0]
				className = ''.join(x.title() for x in moduleName.split('_'))
				try:
					classObject = getattr(import_module(f'resources.{moduleName}'), className)
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
		loggerLevel: str = ConfigConsts.DEFAULT_LOG_LEVEL,
		loggerRotation: str = ConfigConsts.DEFAULT_LOGGER_ROTATION):
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
			accessID = environ[ConfigConsts.DOME9_ACCESS_ID]

		if not secretKey:
			secretKey = environ[ConfigConsts.DOME9_SECRET_KEY]

		Statics.checkIsUUID(arg=accessID)
		Statics.checkOnlyContainsLowercaseAlphanumeric(arg=secretKey)
		Statics.checkIsHTTPURL(arg=baseURL)

		self.loggerLevel = getenv(LoggerConsts.LOG_LEVEL, loggerLevel)
		self.loggerFilePath = getenv(LoggerConsts.LOG_FILE_PATH, loggerPath)
		self.loggerRotation = loggerRotation

		self.headers = {'Accept': ConfigConsts.DEFAULT_FORMAT, 'Content-Type': ConfigConsts.DEFAULT_FORMAT}

		self.baseURL = baseURL if baseURL else ConfigConsts.DEFAULT_BASE_URL
		self.clientAuth = HTTPBasicAuth(username=accessID, password=secretKey)

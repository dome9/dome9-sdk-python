from os import sys

from loguru import logger

from dome9.client import Config


class LoggerController:

	def __init__(self, config: Config):
		self.currentHandler = None
		self.fileHandler = None
		self.level = config.loggerLevel
		self.logFilePath = config.loggerFilePath
		self.rotation = config.loggerRotation
		self.setLevel(level=config.loggerLevel)
		self.logToFile(config.loggerFilePath)
		"""logger controller.

		Args:
			config (Config): D9 client config.
		"""

	def setLevel(self, level):
		self.level = level
		logger.remove(self.currentHandler)
		self.currentHandler = logger.add(sys.stdout, level=self.level)
		if self.fileHandler:
			logger.remove(self.fileHandler)
			logger.add(self.logFilePath, level=self.level, rotation=self.rotation)

	def logToFile(self, logFilePath):
		if logFilePath:
			self.fileHandler = logger.add(logFilePath, level=self.level, rotation=self.rotation)

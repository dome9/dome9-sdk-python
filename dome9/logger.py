from os import sys

from loguru import logger

from dome9.client import Config


class LoggerController:

	def __init__(self, config: Config):
		self.current_handler = None
		self.file_handler = None
		self.level = config.logger_level
		self.log_file_path = config.logger_file_path
		self.rotation = config.logger_rotation
		self.set_level(level=config.logger_level)
		self.log_to_file(config.logger_file_path)
		"""logger controller.

		Args:
			config (Config): D9 client config.

		"""

	def set_level(self, level):
		self.level = level
		logger.remove(self.current_handler)
		self.current_handler = logger.add(sys.stdout, level=self.level)
		if self.file_handler:
			logger.remove(self.file_handler)
			logger.add(self.log_file_path, level=self.level, rotation=self.rotation)

	def log_to_file(self, log_file_path):
		if log_file_path:
			self.file_handler = logger.add(log_file_path, level=self.level, rotation=self.rotation)

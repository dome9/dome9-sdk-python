from re import match


class Statics:

	@staticmethod
	def _checkIsUUID(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', arg):
			raise ValueError

	@staticmethod
	def _checkOnlyContainsLowercaseAlphanumeric(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match('^[0-9a-z]+$', arg):
			raise ValueError

	@staticmethod
	def _checkIsHTTPURL(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(
			r'^(http)s?://(([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+([a-zA-Z]{2,6}\.?|[a-zA-Z0-9-]{2,}\.?)|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)?(/?|[/?]\S+)$',
			arg):
			raise ValueError

	@staticmethod
	def _checkIsARN(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match('^arn:aws[^:]*:[^:]*:[^:]*:[^:]*:[^:]*(:[^:]*)?$', arg):
			raise ValueError

	@staticmethod
	def _checkIsIP(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^(((\d)|([1-9]\d)|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d)|([1-9]\d)|(1\d{2})|(2[0-4]\d)|(25[0-5]))$', arg):
			raise ValueError

	@staticmethod
	def _checkIsDuration(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^((0\.)|([1-9]\d*\.))?((\d)|(1\d)|(2[0-4])):((\d)|([1-5]\d)):((\d)|([1-5]\d))$', arg):
			raise ValueError

	@staticmethod
	def _checkIsEmail(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', arg):
			raise ValueError

	@staticmethod
	def _checkIsUUIDOr12Digits(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^\d{12}$', arg) and not match('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', arg):
			raise ValueError

	@staticmethod
	def _checkIsNotNegative(arg: int, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if arg < 0:
			raise ValueError

	@staticmethod
	def _checkIsNotEmpty(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if arg == '':
			raise ValueError

	@staticmethod
	def _checkIsPort(arg: int, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if arg < 0 or arg > 65535:
			raise ValueError

	@staticmethod
	def getJson(path: str) -> Any:
		"""Creates a Python object from a JSON file.
	
		Args:
			path (str): Path to the file.
	
		Returns:
			Python object.
	
		Raises:
			OSError: Could not read file.
			JSONDecodeError: Could not decode file contents.
		"""

		with open(file=path) as jsonFile:
			return json.load(jsonFile)

from typing import Callable

from re import match


class Statics:

	def __new__(cls: Callable):
		raise BaseException(f'cannot instantiate {cls.__name__} class')

	@staticmethod
	def checkIsUUID(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', arg):
			raise ValueError

	@staticmethod
	def checkOnlyContainsLowercaseAlphanumeric(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match('^[0-9a-z]+$', arg):
			raise ValueError

	@staticmethod
	def checkIsHTTPURL(arg: str, optional: bool = False) -> None:
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
	def checkIsIP(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^(((\d)|([1-9]\d)|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d)|([1-9]\d)|(1\d{2})|(2[0-4]\d)|(25[0-5]))$', arg):
			raise ValueError

	@staticmethod
	def checkIsDuration(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^((0\.)|([1-9]\d*\.))?((\d)|(1\d)|(2[0-4])):((\d)|([1-5]\d)):((\d)|([1-5]\d))$', arg):
			raise ValueError

	@staticmethod
	def checkIsEmail(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', arg):
			raise ValueError

	@staticmethod
	def checkIsUUIDOr12Digits(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^\d{12}$', arg) and not match('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', arg):
			raise ValueError

	@staticmethod
	def checkIsNotNegative(arg: int, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if arg < 0:
			raise ValueError

	@staticmethod
	def checkIsNotEmpty(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if arg == '':
			raise ValueError

	@staticmethod
	def checkIsPort(arg: int, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if arg < 0 or arg > 65535:
			raise ValueError

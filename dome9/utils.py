from typing import Callable, Optional, Dict, List, Union

from re import match

from dome9.consts import AwsRegions, Protocols
from dome9.exceptions import UnsupportedRegionException


class APIUtils:

	def __new__(cls: Callable):
		raise BaseException(f'cannot instantiate {cls.__name__} class')

	@staticmethod
	def check_is_uuid(arg: str, optional: bool = False) -> None:
		if optional:
			return

		if arg is None or not match('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', arg):
			raise ValueError

	@staticmethod
	def check_only_contains_lowercase_alphanumeric(arg: str, optional: bool = False) -> None:
		if optional:
			return

		if arg is None or not match('^[0-9a-z]+$', arg):
			raise ValueError

	@staticmethod
	def check_is_http_url(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(
			r'^(http)s?://(([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+([a-zA-Z]{2,6}\.?|[a-zA-Z0-9-]{2,}\.?)|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)?(/?|[/?]\S+)$',
			arg):
			raise ValueError

	@staticmethod
	def _check_is_arn(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match('^arn:aws[^:]*:[^:]*:[^:]*:[^:]*:[^:]*(:[^:]*)?$', arg):
			raise ValueError

	@staticmethod
	def check_is_ip(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^(((\d)|([1-9]\d)|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d)|([1-9]\d)|(1\d{2})|(2[0-4]\d)|(25[0-5]))$', arg):
			raise ValueError

	@staticmethod
	def check_is_duration(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^((0\.)|([1-9]\d*\.))?((\d)|(1\d)|(2[0-4])):((\d)|([1-5]\d)):((\d)|([1-5]\d))$', arg):
			raise ValueError

	@staticmethod
	def check_is_email(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', arg):
			raise ValueError

	@staticmethod
	def check_is_uuid_or_12_digits(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if not match(r'^\d{12}$', arg) and not match('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', arg):
			raise ValueError

	@staticmethod
	def check_is_not_negative(arg: int, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if arg < 0:
			raise ValueError

	@staticmethod
	def check_is_not_empty(arg: str, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if arg == '':
			raise ValueError

	@staticmethod
	def check_is_port(arg: int, optional: bool = False) -> None:
		if optional and arg is None:
			return

		if arg < 0 or arg > 65535:
			raise ValueError

	@staticmethod
	def check_is_valid_aws_region_id(region: str, optional: bool = False) -> None:
		if optional and region is None:
			return

		regions = [region.value for region in AwsRegions]
		if region not in regions:
			raise UnsupportedRegionException(f'region must be one of the following {regions}')

	@staticmethod
	def check_is_valid_protocol(protocol: str, optional: bool = False) -> None:
		if optional and protocol is None:
			return

		protocols = [protocol.value for protocol in Protocols]
		if protocol not in protocols:
			raise UnsupportedRegionException(f'protocol must be one of the following {Protocols}')


class Utils:
	@staticmethod
	def convert_to_camel_case(str_in_snake_case: str):
		return ''.join(word.title() for word in str_in_snake_case.split('_'))

	@staticmethod
	def convert_to_pascal_case(str_in_snake_case: str):
		str_in_camel_case = Utils.convert_to_camel_case(str_in_snake_case=str_in_snake_case)
		return str_in_camel_case[0].lower() + str_in_camel_case[1:]

	@staticmethod
	def convert_keys_to_camel_case(obj: Union[Dict, List], skip_empty: bool):
		return Utils._convert_keys_to_desired_case(obj=obj, skip_empty=skip_empty, case_func=Utils.convert_to_camel_case)

	@staticmethod
	def convert_keys_to_pascal_case(obj: Union[Dict, List], skip_empty: bool):
		return Utils._convert_keys_to_desired_case(obj=obj, skip_empty=skip_empty, case_func=Utils.convert_to_pascal_case)

	@staticmethod
	def _convert_keys_to_desired_case(obj: Union[Dict, List], skip_empty: bool, case_func: Callable):
			if isinstance(obj, list):
				return [Utils._convert_keys_to_desired_case(obj=elem, skip_empty=skip_empty, case_func=case_func) for elem in obj]
			elif isinstance(obj, dict):
				return {case_func(key): Utils._convert_keys_to_desired_case(value, skip_empty=skip_empty, case_func=case_func) for key, value in obj.items() if
				        not (skip_empty and value is None)}
			else:
				return obj

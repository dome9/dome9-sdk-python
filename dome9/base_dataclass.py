from dataclasses import dataclass

from dataclasses_json import dataclass_json

from dome9.utils import Utils


@dataclass_json
@dataclass
class BaseDataclassRequest:

	def load(self, skip_empty=True):
		return BaseDataclassRequest.convert_keys_to_lowerCase(dict_to_convert=self.to_dict(), skip_empty=skip_empty)

	@staticmethod
	def convert_keys_to_lowerCase(dict_to_convert: dict, skip_empty: bool):
		payload = {}
		for key, value in dict_to_convert.items():
			if isinstance(value, dict):
				value = BaseDataclassRequest.convert_keys_to_lowerCase(dict_to_convert=value, skip_empty=skip_empty)
			# discard unset variables (None) recursively
			if not (skip_empty and value is None):
				payload[Utils.convert_to_camel_case(key)] = value

		return payload

from dataclasses import dataclass

from dataclasses_json import dataclass_json

from dome9.utils import Utils


@dataclass_json
@dataclass
class BaseDataclassRequest:

	def load(self, skip_empty=True):
		return Utils.convert_keys_to_camel_case(obj=self.to_dict(), skip_empty=skip_empty)


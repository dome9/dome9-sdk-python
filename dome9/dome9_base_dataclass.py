from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BaseDataclassRequest:

	def load(self, skip_empty=True):
		# discard unset variables (None) recursively
		return {key: value for key, value in self.to_dict().items() if not (skip_empty and value is None)}

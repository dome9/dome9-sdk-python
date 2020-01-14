from dataclasses import dataclass
from enum import Enum

from dome9 import Client, Dome9Resource, BaseDataclassRequest


class ContinuousComplianceNotificationConsts(Enum):
	MAIN_ROUTE = 'ContinuousCompliancePolicy'


@dataclass
class ContinuousComplianceNotificationRequest(BaseDataclassRequest):
	pass


class ContinuousCompliancePolicy(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client=client)

	def create(self, body):
		self._post(route=ContinuousComplianceNotificationConsts.MAIN_ROUTE.value, body=body)

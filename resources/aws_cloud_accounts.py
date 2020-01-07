from dome9.client import Client
from dome9.dome9_resource import Dome9Resource

from loguru import logger


class AwsCloudAccounts(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def getAWSCloudAccount(self, ID):
		logger.debug(f'getting AWS cloud account ID {ID}')
		self.loggerController.setLevel('DEBUG')
		logger.debug(f'getting AWS cloud account ID 2 {ID}')
		route = f'CloudAccounts/{ID}'
		return self.get(route=route)

from typing import Dict

from resources.ip_list import IpList as BaseIpList, IpListRequest


class ip_list(BaseIpList):

	@classmethod
	def create(cls, body: IpListRequest) -> Dict:
		pass

	@classmethod
	def get(cls, ip_list_id: int) -> Dict:
		pass

	@classmethod
	def update(cls, ip_list_id: int, body: IpListRequest) -> None:
		pass

	@classmethod
	def delete(cls, ip_list_id: int) -> None:
		pass

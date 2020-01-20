from typing import Dict

from resources.ip_list import IpList as BaseIpList, IpListRequest


class ip_list(BaseIpList):

	@classmethod
	def create(cls, body: IpListRequest) -> Dict:
		"""Add a new IP List

		:link   https://api-v2-docs.dome9.com/#iplist_post
		:param  body: IP list details
		:type   body: IpListRequest
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-models-iplistviewmodel
		:rtype  IpList

		"""
		pass

	@classmethod
	def get(cls, ip_list_id: int) -> Dict:
		"""Get an IP List by ID

		:link   https://api-v2-docs.dome9.com/#iplist_get
		:param  ip_list_id: ID of the IP list to get
		:type   ip_list_id: int
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-models-iplistviewmodel
		:rtype  IpList

		"""
		pass

	@classmethod
	def update(cls, ip_list_id: int, body: IpListRequest) -> None:
		"""Update an IP list. This will override the existing IP list

		:link  https://api-v2-docs.dome9.com/#iplist_put
		:param  ip_list_id: ID of the IP list to update
		:type   ip_list_id: int
		:param  body: IP list details
		:type   body: IpListRequest

		"""
		pass

	@classmethod
	def delete(cls, ip_list_id: int) -> None:
		"""Delete an IP List by ID

		:link https://api-v2-docs.dome9.com/#iplist_delete
		:param ip_list_id: ID of the IP list ot delete
		:type  ip_list_id: int

		"""
		pass

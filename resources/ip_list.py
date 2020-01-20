from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from loguru import logger

from dome9 import Dome9Resource, Client, BaseDataclassRequest, APIUtils


class IpListConsts(Enum):
	MAIN_ROUTE = 'IpList'


@dataclass
class IpDescriptorItem(BaseDataclassRequest):
	"""IP list descriptor item

	:link  https://api-v2-docs.dome9.com/#schemafalconetix-model-ipdescriptor
	:param ip: (Required) IP address with CIDR notation (e.g. 10.0.0.0/16 or 10.50.100.22/32) if omitted default of /32 will be assigned
	:type  ip: str
	:param comment: (Optional) IP address description
	:type  comment: str

	"""
	ip: str
	comment: str = None

	@logger.catch(reraise=True)
	def __post_init__(self):
		APIUtils.check_is_ip(self.ip)


@dataclass
class IpListRequest(BaseDataclassRequest):
	"""IP list request: "Name" for name, "Description" for description and Items are list of addresses

	:link  https://api-v2-docs.dome9.com/#schemadome9-web-api-models-iplistviewmodel
	:param name: (Required) IP list name
	:type  name: str
	:param items: (Optional) List of IP descriptor items
	:type  items: list(IpDescriptorItem)
	:param description: (Optional) IP list description
	:type  description: str

	"""
	name: str
	items: List[IpDescriptorItem] = ()
	description: str = None


class IpList(Dome9Resource):

	def __init__(self, client: Client):
		super().__init__(client)

	def create(self, body: IpListRequest) -> Dict:
		"""Add a new IP List

		:link   https://api-v2-docs.dome9.com/#iplist_post
		:param  body: IP list details
		:type   body: IpListRequest
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-models-iplistviewmodel
		:rtype  IpList

		"""

		return self._post(route=IpListConsts.MAIN_ROUTE.value, body=body)

	def get(self, ip_list_id: int) -> Dict:
		"""Get an IP List by ID

		:link   https://api-v2-docs.dome9.com/#iplist_get
		:param  ip_list_id: ID of the IP list to get
		:type   ip_list_id: int
		:return https://api-v2-docs.dome9.com/#schemadome9-web-api-models-iplistviewmodel
		:rtype  IpList

		"""
		route = f'{IpListConsts.MAIN_ROUTE.value}/{ip_list_id}'

		return self._get(route=route)

	def update(self, ip_list_id: int, body: IpListRequest) -> None:
		"""Update an IP list. This will override the existing IP list

		:link  https://api-v2-docs.dome9.com/#iplist_put
		:param  ip_list_id: ID of the IP list to update
		:type   ip_list_id: int
		:param  body: IP list details
		:type   body: IpListRequest

		"""
		route = f'{IpListConsts.MAIN_ROUTE.value}/{ip_list_id}'

		return self._put(route=route, body=body)

	def delete(self, ip_list_id: int) -> None:
		"""Delete an IP List by ID

		:link https://api-v2-docs.dome9.com/#iplist_delete
		:param ip_list_id: ID of the IP list ot delete
		:type  ip_list_id: int

		"""
		route = f'{IpListConsts.MAIN_ROUTE.value}/{ip_list_id}'

		return self._delete(route=route)

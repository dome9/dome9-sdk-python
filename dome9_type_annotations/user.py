from typing import Dict, List, Union

from resources.user import User as BaseAwsCloudAccount, UserRequest, UpdateUser, SetAsOwner


class user(BaseAwsCloudAccount):

	@classmethod
	def create(cls, body: UserRequest) -> Dict:
		"""Create user in dome9

		:param body: Details for the new user
		:type body: UserRequest
		:returns: Dict that has metadata for the created user in dome9

		"""
		pass

	@classmethod
	def get(cls, user_id: str = '') -> Union[Dict, List[Dict]]:
		"""Get all Dome9 users for the Dome9 account.
	
		:link   https://api-v2-docs.dome9.com/index.html#user_get
		:param  user_id: Dome9 user id
		:type   user_id: str
		:return https://api-v2-docs.dome9.com/index.html#schemadome9-web-api-user-userviewmodel
		:rtype  Dict
		"""
		pass

	@classmethod
	def update(cls, user_id: str, body: UpdateUser) -> Dict:
		"""Update the user with the specified id

		:link   https://api-v2-docs.dome9.com/index.html#user_put
		:param  user_id: Dome9 user id
		:type   user_id: str
		:param  body: Details for the user
		:type   body: UpdateUser
		:return 200 OK
		:rtype  Dict
		"""
		pass

	@classmethod
	def set_as_owner(cls, body: SetAsOwner) -> None:
		"""Update users Roles or permissions

		:link
		:param body: Set user as owner details
		:type body: SetAsOwner
		:return: metadata for user object
		:rtype: Dict

		"""
		pass

	@classmethod
	def delete(cls, user_id: str) -> None:
		"""Delete a user

		:link    https://api-v2-docs.dome9.com/index.html#user_delete
		:param   user_id: Dome9 user id
		:type    user_id: str
		:return: None

		"""
		pass

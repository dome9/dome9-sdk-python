from typing import Dict, List

from resources.user import User as BaseAwsCloudAccount, UserRequest, UpdateUser, SetAsOwner


class user(BaseAwsCloudAccount):

	@classmethod
	def create(cls, body: UserRequest) -> Dict:
		pass

	@classmethod
	def get(cls, user_id: str) -> Dict:
		pass

	@classmethod
	def get_all(cls) -> List:
		pass

	@classmethod
	def update(cls, user_id: str, body: UpdateUser) -> Dict:
		pass

	@classmethod
	def set_as_owner(cls, body: SetAsOwner) -> None:
		pass

	@classmethod
	def delete(cls, user_id: str) -> None:
		pass

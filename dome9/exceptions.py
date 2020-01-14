from typing import Optional


class Dome9APIException(Exception):

	def __init__(self, message: str, code: Optional[int] = None, content: Optional[str] = None):
		"""d9 custom exception.

		Args:
			message (str): custom exception message.
			code (int): custom exception code
			content (str): custom exception content.
		"""
		super().__init__(message)
		self.code = code
		self.content = content


class Dome9AccessIDNotFoundException(Exception):
	pass


class Dome9SecretKeyNotFoundException(Exception):
	pass


class UnsupportedRegionException(Exception):
	pass


class UnsupportedCloudAccountCredentialsBasedType(Exception):
	pass


class UnsupportedCloudAccountGroupBehaviors(Exception):
	pass


class UnsupportedProtectionMode(Exception):
	pass


class UnsupportedPolicyType(Exception):
	pass


class UnsupportedCloudAccountEntityType(Exception):
	pass


class UnsupportedRuleEntitySeverity(Exception):
	pass


class UnsupportedCloudVendor(Exception):
	pass


class UnsupportedScheduleDataReportType(Exception):
	pass


class UnsupportedNotificationState(Exception):
	pass


class UnsupportedNotificationOutputFormat(Exception):
	pass


class UnsupportedNotificationSystemType(Exception):
	pass

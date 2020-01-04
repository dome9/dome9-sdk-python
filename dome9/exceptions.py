#!/usr/bin/env python

from typing import Optional


class Dome9APIException(Exception):
	def __init__(self, message: str, code: Optional[int] = None, content: Optional[str] = None):
		super().__init__(message)
		self.code = code
		self.content = content

from typing import Callable, Any


class IterableEnumMeta(type):

	def __getattr__(cls, key: str):
		return cls.__dict__[key]

	def __setattr__(cls, key: str, value: Any):
		raise TypeError(f'Cannot rename const attribute {cls.__name__}.{key}')

	def __getitem__(cls, key: str):
		return cls.__dict__[key]

	def __iter__(cls):
		for key in cls.__dict__:
			if not callable(key) and type(cls.__dict__[key]) != staticmethod and not key.startswith('_'):
				yield cls.__dict__[key]

	def values(cls):
		return list(cls)


class StaticClass:

	def __new__(cls: Callable):
		raise Exception(f'Cannot instantiate Static Class {cls.__name__}')


class Enum(StaticClass, metaclass=IterableEnumMeta):
	pass

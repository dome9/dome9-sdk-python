import os
import pkgutil

__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))

for file in __all__:
	__import__(file, globals(), locals())

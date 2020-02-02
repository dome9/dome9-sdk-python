from setuptools import setup, find_packages
from dome9 import __version__


def readme():
	with open('README.md') as md:
		return md.read()


def requirements():
	with open('requirements.txt') as requirements_file:
		return requirements_file.read().splitlines()


setup(name='dome9',
	description='dome9 py sdk module',
	python_requires='>3.7',
	version=__version__,
	long_description=readme(),
	author='dome9 sre team',
	author_email='d9ops@checkpoint.com',
	license='MIT',
	url='git+https://github.com/Dome9/dome9-sdk-python',
	packages=find_packages(),
	include_package_data=True,
	install_requires=requirements(),
	zip_safe=False)
project_urls = {
	"Repository": "https://github.com/Dome9/dome9-sdk-python",
	"Bug Reports": "https://github.com/Dome9/dome9-sdk-python/issues",
	"Documentation": "https://github.com/Dome9/dome9-sdk-python",
}

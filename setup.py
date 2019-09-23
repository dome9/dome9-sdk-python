import io

from setuptools import setup, find_packages


def readme():
	with open('README.md') as md:
		return md.read()


about = {}
with io.open('dome9_sdk_python/_version.py', 'r', encoding='utf-8') as f:
	exec (f.read(), about)

setup(name='dome9_sdk_python',
	description='Dome9 api module',
	version=about['__version__'],
	long_description=readme(),
	author='Udi-Yehuda Tamar & Cfir Carmeli',
	author_email='d9ops@checkpoint.com',
	license='MIT',
	url='git+https://github.com/Dome9/dome9-sdk-python',
	packages=find_packages(),
	include_package_data=True,
	install_requires=[
		'requests'
	],
	zip_safe=False)
project_urls = {
			   "Repository"   : "https://github.com/Dome9/dome9-sdk-python",
			   "Bug Reports"  : "https://github.com/Dome9/dome9-sdk-python/issues",
			   "Documentation": "https://github.com/Dome9/dome9-sdk-python",
		   },

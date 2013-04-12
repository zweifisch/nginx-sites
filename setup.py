# from distutils.core import setup
from setuptools import setup

setup(
	name='nginx-sites',
	url='https://github.com/zweifisch/nginx-sites',
	version='0.0.1',
	description='cli utility for managing nginx site configs',
	author='Feng Zhou',
	author_email='zf.pascal@gmail.com',
	packages=['nginxSites'],
	install_requires=['docopt', 'blessings', 'pystache'],
	entry_points={
		'console_scripts': ['nginx-sites=nginxSites:main'],
	},
)
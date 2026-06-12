from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in nesscale_awesome/__init__.py
from nesscale_awesome import __version__ as version

setup(
	name="nesscale_awesome",
	version=version,
	description="Nesscale Utility",
	author="Nesscale Solutions Pvt Ltd",
	author_email="info@nesscale.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

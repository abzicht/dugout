from setuptools import find_packages, setup
from distutils.core import setup

setup(
    name='dugoutserver',
    author='abzicht',
    version="0.0.0",
    author_email='abzicht@gmail.com',
    description=('RS485 Temperature and Humidity Raspberry Server'),
    license='mit',
    include_package_data=False,
    packages=find_packages(),
    install_requires=[],
    entry_points={'console_scripts': [
        'dugout-server=dugoutserver.script:main',
    ]},
)


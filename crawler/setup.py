from setuptools import find_packages, setup
from distutils.core import setup

setup(
    name='dugoutcrawler',
    author='abzicht',
    version="0.0.0",
    author_email='abzicht@gmail.com',
    description=('Crawler pulling data of the dugoutserver and pushing it to elasticsearch'),
    license='mit',
    include_package_data=False,
    packages=find_packages(),
    install_requires=['apscheduler', 'elasticsearch', 'meteocalc'],
    entry_points={'console_scripts': [
        'dugout-crawler=dugoutcrawler.script:main',
    ]},
)


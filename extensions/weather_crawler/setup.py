from setuptools import find_packages, setup
from distutils.core import setup

setup(
    name='dugoutweathercrawler',
    author='abzicht',
    version="0.0.0",
    author_email='abzicht@gmail.com',
    description=('Crawler pulling weather data from openweathermap and pushing it to elasticsearch'),
    license='mit',
    include_package_data=False,
    packages=find_packages(),
    install_requires=['apscheduler==3.10.1', 'elastic-transport', 'elasticsearch', 'meteocalc', 'pyowm'],
    entry_points={'console_scripts': [
        'dugout-weather-crawler=dugoutweathercrawler.script:main',
    ]},
)


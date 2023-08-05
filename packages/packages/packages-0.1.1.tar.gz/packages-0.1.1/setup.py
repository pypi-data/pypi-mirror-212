# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['packages', 'packages.aggs', 'packages.commands']

package_data = \
{'': ['*']}

install_requires = \
['cached_property>=1.5.1,<2.0.0',
 'click>=7.0,<8.0',
 'lxml>=4.4.2,<5.0.0',
 'pymongo>=3.10.0,<4.0.0',
 'redis>=3.3.11,<4.0.0',
 'requests-cache>=0.5.2,<0.6.0',
 'requests>=2.22.0,<3.0.0',
 'tqdm>=4.40.2,<5.0.0']

entry_points = \
{'console_scripts': ['packages = packages.cli:cli']}

setup_kwargs = {
    'name': 'packages',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Chris Hunt',
    'author_email': 'chrahunt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

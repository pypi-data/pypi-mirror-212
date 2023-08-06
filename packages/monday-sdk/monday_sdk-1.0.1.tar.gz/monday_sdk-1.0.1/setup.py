# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monday_sdk']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.88.0,<0.89.0', 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'monday-sdk',
    'version': '1.0.1',
    'description': '',
    'long_description': '# Python SDK for monday.com\n',
    'author': 'Jonathan Crum',
    'author_email': 'jcrum@theobogroup.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/krummja/MondaySDK.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

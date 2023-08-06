# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['extras_py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'extras-py',
    'version': '0.1.2',
    'description': 'Adding in simple things that are tedious to add in on your own, with one simple line you can unlock easiness.',
    'long_description': None,
    'author': 'SalladShooter',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

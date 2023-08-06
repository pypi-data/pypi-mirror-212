# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tca_beam']

package_data = \
{'': ['*'], 'tca_beam': ['templates/*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'jinja2>=3.1.2,<4.0.0']

entry_points = \
{'console_scripts': ['tca-beam = tca_beam.tca_beam:start']}

setup_kwargs = {
    'name': 'tca-beam',
    'version': '0.3.4',
    'description': 'Feature stub generation for The Composable Architecture',
    'long_description': 'This is a proof-of-concept implementation of [Scaffold for The Composable Architecture](../README.md) in Python.\n\nWork in progress!\n\n\n',
    'author': 'Alex Hunsley',
    'author_email': 'alex.hunsley@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

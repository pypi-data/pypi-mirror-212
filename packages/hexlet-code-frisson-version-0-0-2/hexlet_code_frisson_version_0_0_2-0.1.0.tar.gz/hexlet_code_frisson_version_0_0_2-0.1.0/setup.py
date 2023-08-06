# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brain_games', 'brain_games.scripts']

package_data = \
{'': ['*']}

install_requires = \
['prompt>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['brain-games = brain_games.scripts.brain_games:main']}

setup_kwargs = {
    'name': 'hexlet-code-frisson-version-0-0-2',
    'version': '0.1.0',
    'description': '',
    'long_description': '### Hexlet tests and linter status:\n[![Actions Status](https://github.com/FrissonFrisson/python-project-49/workflows/hexlet-check/badge.svg)](https://github.com/FrissonFrisson/python-project-49/actions)',
    'author': 'FrissonFrisson',
    'author_email': 'compton56rus@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

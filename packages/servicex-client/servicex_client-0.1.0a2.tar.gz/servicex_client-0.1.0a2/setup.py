# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['servicex_client', 'servicex_client.app', 'servicex_client.func_adl']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'func_adl==3.2.5-alpha.1',
 'google-auth>=2.17,<3.0',
 'httpx>=0.24,<0.25',
 'miniopy-async>=1.15,<2.0',
 'pydantic>=1.10,<2.0',
 'qastle>=0.16,<0.17',
 'requests>=2.31,<3.0',
 'tinydb>=4.7,<5.0',
 'typer[all]>=0.9.0,<0.10.0',
 'types-PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['servicex = servicex_client.app.main:app']}

setup_kwargs = {
    'name': 'servicex-client',
    'version': '0.1.0a2',
    'description': '',
    'long_description': '# servicex_client\nPython SDK and CLI Client for ServiceX\n',
    'author': 'Ben Galewsky',
    'author_email': 'bengal1@illinois.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)

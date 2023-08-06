# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dmodel', 'dmodel.functions', 'dmodel.models']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.2,<4.0.0',
 'dhint>=0.0.9,<0.0.10',
 'dtbase>=0.0.4,<0.0.5',
 'python-multipart>=0.0.6,<0.0.7',
 'smartjs>=0.1.6,<0.2.0',
 'typing-extensions>=4.6.2,<5.0.0',
 'uvicorn>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'dmodel',
    'version': '0.0.6',
    'description': 'models for deta space',
    'long_description': None,
    'author': 'Daniel Arantes',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

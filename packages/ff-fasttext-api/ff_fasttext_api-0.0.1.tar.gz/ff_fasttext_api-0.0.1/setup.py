# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ff_fasttext_api', 'ff_fasttext_api.scripts', 'scripts']

package_data = \
{'': ['*']}

install_requires = \
['bonn>=0.1,<0.2',
 'click>=8.0.3,<9.0.0',
 'dynaconf>=3.1.7,<4.0.0',
 'fastapi>=0.93,<0.94',
 'httpx>=0.24.0,<0.25.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'ruff>=0.0.264,<0.0.265',
 'starlette>=0.25.0,<0.26.0',
 'structlog>=21.5,<22.0',
 'urllib3>=1.26,<2.0',
 'uvicorn>=0.17.4,<0.18.0']

entry_points = \
{'console_scripts': ['ff_fasttext_cli = '
                     'ff_fasttext_api.scripts.ff_fasttext:main']}

setup_kwargs = {
    'name': 'ff-fasttext-api',
    'version': '0.0.1',
    'description': "Created for ONS. API/CLI wrapper for proof-of-concept mmap'd Rust word2vec implementation linked with category matching",
    'long_description': None,
    'author': 'Phil Weir',
    'author_email': 'phil.weir@flaxandteal.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)

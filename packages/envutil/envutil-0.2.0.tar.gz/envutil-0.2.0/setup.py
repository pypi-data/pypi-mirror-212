# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['envutil']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'envutil',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'Berke Arslan',
    'author_email': 'berke@kwilabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

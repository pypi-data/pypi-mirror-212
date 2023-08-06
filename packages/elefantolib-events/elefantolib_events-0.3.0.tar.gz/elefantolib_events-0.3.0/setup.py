# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elefantolib_events']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=9.1.2,<10.0.0', 'orjson>=3.9.0,<4.0.0']

setup_kwargs = {
    'name': 'elefantolib-events',
    'version': '0.3.0',
    'description': '',
    'long_description': '',
    'author': 'Aibar',
    'author_email': 'bekaybar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

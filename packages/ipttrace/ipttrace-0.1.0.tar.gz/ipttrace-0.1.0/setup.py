# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipttrace']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.6.0,<13.0.0', 'typer>=0.9.0,<0.10.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['ipttrace = ipttrace.main:app']}

setup_kwargs = {
    'name': 'ipttrace',
    'version': '0.1.0',
    'description': 'trace iptables rules with ease',
    'long_description': None,
    'author': 'sieginglion',
    'author_email': 'sieginglion@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.3,<4.0.0',
}


setup(**setup_kwargs)

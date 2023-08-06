# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jquants_derivatives']

package_data = \
{'': ['*']}

install_requires = \
['jquants-api-client>=1.2.0,<2.0.0', 'plotly>=5.14.1,<6.0.0']

setup_kwargs = {
    'name': 'jquants-derivatives',
    'version': '0.1.0a1',
    'description': '',
    'long_description': '# jquants-derivatives\n',
    'author': 'driller',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

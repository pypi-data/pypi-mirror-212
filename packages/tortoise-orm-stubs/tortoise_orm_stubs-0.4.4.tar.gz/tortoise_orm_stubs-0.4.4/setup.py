# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tortoise-stubs']

package_data = \
{'': ['*'], 'tortoise-stubs': ['fields/*']}

install_requires = \
['tortoise-orm']

setup_kwargs = {
    'name': 'tortoise-orm-stubs',
    'version': '0.4.4',
    'description': 'Type stubs that make tortoise-orm a lot easier to work with when using type checkers.',
    'long_description': "# tortoise-orm-stubs\n\nType stubs that make **tortoise-orm** a bit easier to work with when using type checkers.\n\nSpecifically, data fields' types automatically reflect the value of null argument (i.e. become optional if you set null=True)\n\n## Installation\n\n`pip install tortoise-orm-stubs`\n\n## Disclaimer\n\nPreviously **tortoise-orm-stubs** provided a lot more value but now the majority of its functionality has become a part of **tortoise-orm**. Hopefully, it will become completely unnecessary in the future.\n",
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ovsyanka83/tortoise-orm-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

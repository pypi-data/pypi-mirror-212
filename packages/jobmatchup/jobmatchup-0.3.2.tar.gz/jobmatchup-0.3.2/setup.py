# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jobmatchup',
 'jobmatchup.api',
 'jobmatchup.configs',
 'jobmatchup.entity',
 'jobmatchup.errors',
 'jobmatchup.storage',
 'jobmatchup.tools']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.8.14,<4.0.0',
 'pydantic>=1.10.8,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'jobmatchup',
    'version': '0.3.2',
    'description': 'Personal Vacancies Parse',
    'long_description': '<p align="center">\n  <img alt="" src="https://i.ibb.co/6XWd58N/python-applications-removebg.png" width="500px">\n</p>\t\n\n***\n### about\n\n> Personal vacancies Parser\n\n<details>\n <summary>What sites can you parse from?</summary>\n<ul>\n  <li>hh.ru :heavy_check_mark:</li>\n  <li>superjob.ru :heavy_check_mark:</li>\n</ul>\n</details>\n\n***\n\n## install\n\n`pip install jobmatchup`\n\n***\n\n### usage\n\n`see examples` [> Examples <](https://github.com/bbt-t/pvp/tree/main/examples)\n',
    'author': 'bbt-t',
    'author_email': 'zlukcss@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bbt-t/jobmatchup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

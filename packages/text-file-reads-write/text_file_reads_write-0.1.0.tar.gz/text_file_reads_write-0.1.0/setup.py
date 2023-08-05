# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_file_reads_write']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'text-file-reads-write',
    'version': '0.1.0',
    'description': '文本文件批量读取器',
    'long_description': '# text_file_reads_write\n 文本文件批量读取器\n',
    'author': 'ziru-w',
    'author_email': '77319678+ziru-w@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)

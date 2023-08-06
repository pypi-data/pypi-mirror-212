# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysaltcorn']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pysaltcorn',
    'version': '0.3.1',
    'description': 'Python library for Saltcorn API',
    'long_description': '# PySaltcorn\n\nThis is python client interface for [Saltcorn](https://github.com/saltcorn/saltcorn/) REST API.\n\n## Installation\n\n```console\n$ pip3 install pysaltcorn==0.3.1\n```\n\n## Usage\n\n```python\n>>> import io, pysaltcorn; from pprint import pp\n>>> cl = pysaltcorn.SaltcornClient("https://url-encoded-email:password@tenant.saltcorn.com")\n>>> cl.login_session()\n>>> cl.files_upload({\'filename.txt\': io.StringIO(\'file content\\n\')}, \'/foldername/\')\nTrue\n>>> pp(cl.files_list())\n[{\'filename\': \'foldername\',\n  \'location\': \'/root/.local/share/saltcorn/netbox/foldername\',\n  \'uploaded_at\': \'2023-06-08T12:20:25.323Z\',\n  \'size_kb\': 4,\n  \'user_id\': None,\n  \'mime_super\': \'\',\n  \'mime_sub\': \'\',\n  \'min_role_read\': 10,\n  \'s3_store\': False,\n  \'isDirectory\': True}]\n```\n',
    'author': 'Michael Dubner',
    'author_email': 'pywebmail@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

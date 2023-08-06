# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_nested_mutable', 'sqlalchemy_nested_mutable.testing']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2-binary>=2.9.6,<3.0.0',
 'pydantic>=1.10.8,<2.0.0',
 'sqlalchemy>=2.0,<3.0']

setup_kwargs = {
    'name': 'sqlalchemy-nested-mutable',
    'version': '0.0.1',
    'description': 'SQLAlchemy Nested Mutable Types.',
    'long_description': 'SQLAlchemy-Nested-Mutable\n=========================\n\nAn advanced SQLAlchemy column type factory that helps map complex Python types (e.g. List, Dict, Pydantic Model and their hybrids) to database types (e.g. ARRAY, JSONB),\nAnd keep track of mutations in deeply nested data structures so that SQLAlchemy can emit proper UPDATE statements.\n\nSQLAlchemy-Nested-Mutable is highly inspired by SQLAlchemy-JSON <sup>[[0]](https://github.com/edelooff/sqlalchemy-json)</sup><sup>[[1]](https://variable-scope.com/posts/mutation-tracking-in-nested-json-structures-using-sqlalchemy)</sup>. However, it does not limit the mapped Python types to dict-like objects.\n\nDocumentation is not ready yet. Please refer to these test files for usage:\n\n* test_mutable_list.py\n* test_mutable_dict.py\n* test_mutable_pydantic_type.py\n',
    'author': 'Wonder',
    'author_email': 'wonderbeyond@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wonderbeyond/sqlalchemy-nested-mutable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

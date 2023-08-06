# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_nested_mutable', 'sqlalchemy_nested_mutable.testing']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2-binary>=2.8,<3.0',
 'pydantic>=1.10.0,<2.0.0',
 'sqlalchemy>=2.0,<3.0',
 'typing-extensions>=4.5.0,<5.0.0']

setup_kwargs = {
    'name': 'sqlalchemy-nested-mutable',
    'version': '0.1.0',
    'description': 'SQLAlchemy Nested Mutable Types.',
    'long_description': 'SQLAlchemy-Nested-Mutable\n=========================\n\nAn advanced SQLAlchemy column type factory that helps map compound Python types (e.g. `list`, `dict`, *Pydantic Model* and their hybrids) to database types (e.g. `ARRAY`, `JSONB`),\nAnd keep track of mutations in deeply nested data structures so that SQLAlchemy can emit proper *UPDATE* statements.\n\nSQLAlchemy-Nested-Mutable is highly inspired by SQLAlchemy-JSON<sup>[[0]](https://github.com/edelooff/sqlalchemy-json)</sup><sup>[[1]](https://variable-scope.com/posts/mutation-tracking-in-nested-json-structures-using-sqlalchemy)</sup>.\nHowever, it does not limit the mapped Python type to be `dict` or `list`.\n\n---\n\n## Why this package?\n\n* By default, SQLAlchemy does not track in-place mutations for non-scalar data types\n  such as `list` and `dict` (which are usually mapped with `ARRAY` and `JSON/JSONB`).\n\n* Even though SQLAlchemy provides [an extension](https://docs.sqlalchemy.org/en/20/orm/extensions/mutable.html)\n  to track mutations on compound objects, it\'s too shallow, i.e. it only tracks mutations on the first level of the compound object.\n\n* There exists the [SQLAlchemy-JSON](https://github.com/edelooff/sqlalchemy-json) package\n  to help track mutations on nested `dict` or `list` data structures.\n  However, the db type is limited to `JSON(B)`.\n\n* Also, I would like the mapped Python types can be subclasses of the Pydantic BaseModelModel,\n  which have strong schemas, with the db type be schema-less JSON.\n\n\n## Installation\n\n```shell\npip install sqlalchemy-nested-mutable\n```\n\n## Usage\n\n> NOTE the example below is first updated in `examples/user-addresses.py` and then updated here.\n\n```python\nfrom typing import Optional, List\n\nimport pydantic\nimport sqlalchemy as sa\nfrom sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column\nfrom sqlalchemy_nested_mutable import MutablePydanticBaseModel\n\n\nclass Base(DeclarativeBase):\n    pass\n\n\nclass Addresses(MutablePydanticBaseModel):\n    """A container for storing various addresses of users.\n\n    NOTE: for working with pydantic model, use a subclass of `MutablePydanticBaseModel` for column mapping.\n    However, the nested models (e.g. `AddressItem` below) should be direct subclasses of `pydantic.BaseModel`.\n    """\n\n    class AddressItem(pydantic.BaseModel):\n        street: str\n        city: str\n        area: Optional[str]\n\n    preferred: AddressItem\n    work: Optional[AddressItem]\n    home: Optional[AddressItem]\n    others: List[AddressItem] = []\n\n\nclass User(Base):\n    __tablename__ = "user_account"\n\n    id: Mapped[int] = mapped_column(primary_key=True)\n    name: Mapped[str] = mapped_column(sa.String(30))\n    addresses: Mapped[Addresses] = mapped_column(Addresses.as_mutable(), nullable=True)\n\n\nengine = sa.create_engine("sqlite://")\nBase.metadata.create_all(engine)\n\nwith Session(engine) as s:\n    s.add(u := User(name="foo", addresses={"preferred": {"street": "bar", "city": "baz"}}))\n    assert isinstance(u.addresses, MutablePydanticBaseModel)\n    s.commit()\n\n    u.addresses.preferred.street = "bar2"\n    s.commit()\n    assert u.addresses.preferred.street == "bar2"\n\n    u.addresses.others.append(Addresses.AddressItem.parse_obj({"street": "bar3", "city": "baz3"}))\n    s.commit()\n    assert isinstance(u.addresses.others[0], Addresses.AddressItem)\n\n    print(u.addresses.dict())\n```\n\nFor more usage, please refer to the following test files:\n\n* tests/test_mutable_list.py\n* tests/test_mutable_dict.py\n* tests/test_mutable_pydantic_type.py\n',
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

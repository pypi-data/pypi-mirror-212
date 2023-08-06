# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easy_sqla', 'easy_sqla.db', 'tests', 'tests.db']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0',
 'SQLAlchemy==1.4.41',
 'cfgv==3.3.1',
 'distlib==0.3.6',
 'filelock>=3.8.0,<4.0.0',
 'greenlet==1.1.3',
 'identify==2.5.5',
 'jsonformatter==0.3.1',
 'nodeenv==1.7.0',
 'platformdirs==2.5.2',
 'psycopg2==2.9.3',
 'pydantic==1.10.2',
 'toml==0.10.2',
 'typing-extensions==4.3.0']

setup_kwargs = {
    'name': 'easy-sqla',
    'version': '0.1.1',
    'description': 'A wrapper on top of sqlalchemy that allow to make django orm style query',
    'long_description': '# Sqlalchemy-django-wrapper\n\nSQLAlchemy-django-wrapper is a Python library intended to make beautiful SQLAlchemy query syntax.\n\nSQLAlchemy is an awesome and powerful ORM which mades interaction with database very painless. However powerful, sometime mean complex to use.\nThat\'s why the plugin has been built.\n\nIt add extra capabilities to sqla Base model in order to make query effortlessly more simple and readable.\n\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.\n\n```bash\npip install sqlalchemy-django-wrapper\n```\n\n## Usage\n\nsetup.py\n\n```python\nfrom easy_sqla.db.settings import DBSettings\nfrom easy_sqla.db.settings import DriverEnum\nfrom easy_sqla.manager import Manager\n\ndb_settings = DBSettings(\n    driver=DriverEnum.POSTGRESQL,\n    host="your_host",\n    password="password",\n    port="5432",\n    username="user",\n    name="my_db",\n    auto_commit=True  # By default True\n\n)\n\n# Or if you want sqlite database\ndb_settings = DBSettings(\n    driver=DriverEnum.SQLITE,\n    sqlite_db_path="my/path/db.sqlite3"\n\n)\n\n```\n\nNow we\'re going to create all of ours model from the base_model\nmodels.py\n```python\nfrom sqlalchemy import Column\nfrom sqlalchemy import ForeignKey\nfrom sqlalchemy import Integer\nfrom sqlalchemy import String\nfrom sqlalchemy.orm import relationship\n\nfrom tests.base_model import base_model\n\n\nclass Item(base_model):\n    __tablename__ = "item"\n    item_id = Column(Integer, primary_key=True)\n    content = Column(String)\n\n    file = relationship("File")\n\n\nclass File(base_model):\n    __tablename__ = "file"\n\n    id = Column(Integer, primary_key=True)\n    path = Column(String)\n    item = Column(ForeignKey(Item.item_id))\n\n    user = relationship("User")\n\n\nclass User(base_model):\n    __tablename__ = "user_account"\n\n    id = Column(Integer, primary_key=True)\n    first_name = Column(String(50))\n    last_name = Column(String(50))\n    last_login = Column(Datetime)\n    description = Column(String(255))\n    file = Column(ForeignKey(File.id))\n\n    def __repr__(self):\n        return f"User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"\n\n```\nNote that, models above are nested by only ForeignKey. It\'s only for demonstration purposes\nBut the lib will work on relation as well.\n\nservice.py\n```python\nfrom models import User\n\n\n# Get all user\nUser.all()\n\n# Get user when id is greater than 10\n\nUser.filter(id__gt=10)\n\n# Filter by some word in the description\nUser.filter(description__contains="my word")\n\n# Get users which connected between two datetime\nUser.filter(last_login__between=["yyyy/MM/dd", "yyyy/MM/dd",])\n\n# You can also search through a relationship \n# Get all user who have a file which path start by "/var/www"\nUser.filter(file__path__startswith="/var/www")\n\n# No matter the depth of the relationships, you can go through\nUser.filter(file__item__content__contains="my_tag")\n\n```\n**N.B:** You can use almost all operator available originally by sqlalchemy. Complete list below\n\nSometime you would want to add more clause into your query with and/or term. The right is there for that\n\n```python\n\n# When you want only use and, you don\'t need any extra. You build your query in kwargs\n\nUser.filter(my_field="value", my_another_field="value2", ...)\n\n# If you want use or\nfrom easy_sqla.db.operator import Or\n\nUser.filter(Or(my_field="value", my_field2="value2"))\n# will produce following sql query: select * ...... where my_field=\'value\' or my_field2=\'value2\'\n\n\n```\n\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first\nto discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'Soumaila',
    'author_email': 'admin@cloudmali.ml',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_join_unrelated']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-join-unrelated',
    'version': '0.1.0.dev1',
    'description': 'Join Django ORM models having no relations.',
    'long_description': '# django-join-unrelated\nJoin Django ORM models having no relations\n',
    'author': 'Denis Kazakov',
    'author_email': 'denis@kazakov.ru.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/django-join-unrelated',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

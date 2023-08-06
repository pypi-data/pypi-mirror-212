# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lassen',
 'lassen.alembic',
 'lassen.assets',
 'lassen.core',
 'lassen.db',
 'lassen.tests',
 'lassen.tests.fixtures',
 'lassen.tests.fixtures.test_harness.test_harness',
 'lassen.tests.fixtures.test_harness.test_harness.migrations']

package_data = \
{'': ['*'], 'lassen.tests.fixtures': ['test_harness/*']}

install_requires = \
['SQLAlchemy>=2.0.15,<3.0.0',
 'alembic-autogenerate-enums>=0.1.1,<0.2.0',
 'alembic>=1.11.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'fastapi>=0.96.0,<0.97.0',
 'inflection>=0.5.1,<0.6.0',
 'psycopg2>=2.9.6,<3.0.0',
 'pydantic>=1.10.8,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['migrate = lassen.alembic.cli:main']}

setup_kwargs = {
    'name': 'lassen',
    'version': '0.1.0',
    'description': 'Common webapp scaffolding.',
    'long_description': '# lassen\n\n**40.4881° N, 121.5049° W**\n\nCore utilities for MonkeySee web applications.\n\nNot guaranteed to be backwards compatible, use at your own risk.\n\n## Structure\n\n**Stores:** Each model is expected to have its own store. Base classes that provide standard logic are provided by `lassen.store`\n- StoreBase: Base class for all stores\n- StoreFilterMixin: Mixin for filtering stores that specify an additional schema to use to filter\n\n**Migrations:** Lassen includes a templated alembic.init and env.py file. Client applications just need to have a `migrations` folder within their project root. After this you can swap `poetry run alembic` with `poetry run migrate`.\n\n```sh\npoetry run migrate upgrade head\n```\n\n**Settings:** Application settings should subclass our core settings. This provides a standard way to load settings from environment variables and includes common database keys.\n\n```python\nfrom lassen.core.config import CoreSettings, register_settings\n\n@register_settings\nclass ClientSettings(CoreSettings):\n    pass\n```\n\n**Schemas:** For helper schemas when returning results via API, see [lassen.schema](./lassen/schema.py).\n\n## Development\n\n```sh\npoetry install\n\ncreateuser lassen\ncreatedb -O lassen lassen_db\ncreatedb -O lassen lassen_test_db\n```\n\nUnit Tests:\n\n```sh\npoetry run pytest\n```\n',
    'author': 'Pierce Freeman',
    'author_email': 'pierce@freeman.vc',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

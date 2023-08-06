# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renard',
 'renard.pipeline',
 'renard.pipeline.corefs',
 'renard.resources.hypocorisms',
 'renard.resources.pronouns',
 'renard.resources.titles']

package_data = \
{'': ['*'], 'renard.resources.hypocorisms': ['datas/*']}

install_requires = \
['matplotlib>=3.5.3,<4.0.0',
 'more-itertools>=8.12.0,<9.0.0',
 'nameparser>=1.1.0,<2.0.0',
 'networkx>=2.6.3,<3.0.0',
 'nltk>=3.6.5,<4.0.0',
 'pandas>=1.4.4,<2.0.0',
 'pytest>=7.2.1,<8.0.0',
 'seqeval==1.2.2',
 'torch>=1.10.2,<2.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'transformers>=4.11.3,<5.0.0']

extras_require = \
{'spacy': ['spacy>=3.5.0,<4.0.0',
           'coreferee>=1.4.0,<2.0.0',
           'spacy-transformers>=1.2.1,<2.0.0'],
 'stanza': ['stanza>=1.3.0,<2.0.0']}

setup_kwargs = {
    'name': 'renard-pipeline',
    'version': '0.1.0',
    'description': 'Relationships Extraction from NARrative Documents',
    'long_description': '# Renard\n\nRelationships Extraction from NARrative Documents\n\n\n# Installation\n\nYou can install the latest version using pip:\n\n> pip install renard-pipeline\n\n\n# Documentation\n\nDocumentation, including installation instructions, can be found at https://compnet.github.io/Renard/\n\nIf you need local documentation, it can be generated using `Sphinx`. From the `docs` directory, `make html` should create documentation under `docs/_build/html`. \n\n\n# Running tests \n\n`Renard` uses `pytest` for testing. To launch tests, use the following command : \n\n> poetry run python -m pytest tests\n\nExpensive tests are disabled by default. These can be run by setting the environment variable `RENARD_TEST_ALL` to `1`.\n',
    'author': 'Arthur Amalvy',
    'author_email': 'arthur.amalvy@univ-avignon.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

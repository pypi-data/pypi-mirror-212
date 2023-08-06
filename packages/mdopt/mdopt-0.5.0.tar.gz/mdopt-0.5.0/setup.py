# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdopt', 'mdopt.contractor', 'mdopt.mps', 'mdopt.optimiser', 'mdopt.utils']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.12,<10.0',
 'numpy<1.24',
 'opt-einsum>=3.3.0,<4.0.0',
 'qecsim>=1.0b9,<2.0',
 'qecstruct>=0.2.9,<0.3.0',
 'scipy>=1.9.2,<2.0.0',
 'threadpoolctl>=3.1.0,<4.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'mdopt',
    'version': '0.5.0',
    'description': 'Discrete optimisation in the tensor-network (specifically, MPS-MPO) language.',
    'long_description': '[![codecov](https://codecov.io/gh/quicophy/mdopt/branch/main/graph/badge.svg?token=4G7VWYX0S2)](https://codecov.io/gh/quicophy/mdopt)\n[![tests](https://github.com/quicophy/mdopt/actions/workflows/tests.yml/badge.svg)](https://github.com/quicophy/mdopt/actions/workflows/tests.yml)\n[![Documentation Status](https://readthedocs.org/projects/mdopt/badge/?version=latest)](https://mdopt.readthedocs.io/en/latest/?badge=latest)\n[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/quicophy/mdopt/main.svg)](https://results.pre-commit.ci/latest/github/quicophy/mdopt/main)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# mdopt\nmdopt is a python package built on top of numpy for discrete optimisation in the tensor-network (specifically, MPS-MPO) language. The code is hosted on github, so please feel free to submit issues and pull requests.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install mdopt.\n\n```bash\npip install mdopt\n```\n\n## Usage\n\nFor usage, see the examples folder.\n\n## Cite\n```\n@software{mdopt2022,\n  author = {Aleksandr Berezutskii},\n  title = {mdopt: Discrete optimization in the tensor-network (specifically, MPS-MPO) language.},\n  url = {https://github.com/quicophy/mdopt},\n  year = {2022},\n}\n```\n',
    'author': 'Aleksandr Berezutskii',
    'author_email': 'berezutskii.aleksandr@gmail.com',
    'maintainer': 'Aleksandr Berezutskii',
    'maintainer_email': 'berezutskii.aleksandr@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

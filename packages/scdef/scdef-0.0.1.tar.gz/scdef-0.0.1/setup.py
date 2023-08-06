# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scdef', 'scdef.models']

package_data = \
{'': ['*']}

install_requires = \
['anndata>=0.9.1,<0.10.0',
 'click>=8.0.1,<9.0.0',
 'graphviz>=0.14.2,<0.15.0',
 'gseapy>=1.0.4,<2.0.0',
 'jax>=0.3.20,<0.4.0',
 'jaxlib>=0.3.20,<0.4.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'scanpy>=1.9.3,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['scdef = scdef:main']}

setup_kwargs = {
    'name': 'scdef',
    'version': '0.0.1',
    'description': 'Extract hierarchical signatures of cell state from single-cell data.',
    'long_description': '<div align="left">\n  <img src="https://github.com/cbg-ethz/scDEF/raw/main/figures/scdef.png", width="300px">\n</div>\n<p></p>\n<!--\n[![pypi](https://img.shields.io/pypi/v/scdef.svg?style=flat)](https://pypi.python.org/pypi/scdef)\n[![build](https://github.com/pedrofale/scdef/actions/workflows/main.yaml/badge.svg)](https://github.com/pedrofale/scDEF/actions/workflows/main.yaml) -->\n\nDeep exponential families for single-cell data.\n',
    'author': 'pedrofale',
    'author_email': 'pedro.miguel.ferreira.pf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cbg-ethz/scdef',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)

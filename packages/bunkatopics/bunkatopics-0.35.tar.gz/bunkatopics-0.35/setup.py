# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bunkatopics',
 'bunkatopics.bunka_logger',
 'bunkatopics.functions',
 'bunkatopics.visualisation']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.3.0,<24.0.0',
 'gensim>=4.3.1,<5.0.0',
 'hdbscan>=0.8.29,<0.9.0',
 'instructorembedding>=1.0.1,<2.0.0',
 'ipywidgets>=8.0.6,<9.0.0',
 'jupyterlab>=4.0.1,<5.0.0',
 'kneed>=0.8.3,<0.9.0',
 'langchain>=0.0.188,<0.0.189',
 'loguru>=0.7.0,<0.8.0',
 'matplotlib>=3.7.1,<4.0.0',
 'pandas>=2.0.2,<3.0.0',
 'plotly>=5.14.1,<6.0.0',
 'sentence-transformers>=2.2.2,<3.0.0',
 'statsmodels>=0.14.0,<0.15.0',
 'textacy>=0.13.0,<0.14.0',
 'umap-learn>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'bunkatopics',
    'version': '0.35',
    'description': 'Topic Modeling using Transformers and advanced visualization',
    'long_description': '',
    'author': 'Charles De Dampierre',
    'author_email': 'charlesdedampierre@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

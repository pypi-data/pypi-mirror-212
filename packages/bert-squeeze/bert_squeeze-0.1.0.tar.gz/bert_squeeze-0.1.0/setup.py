# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bert_squeeze',
 'bert_squeeze.assistants',
 'bert_squeeze.data',
 'bert_squeeze.data.local_datasets',
 'bert_squeeze.data.modules',
 'bert_squeeze.distillation',
 'bert_squeeze.distillation.utils',
 'bert_squeeze.inference',
 'bert_squeeze.models',
 'bert_squeeze.models.custom_transformers',
 'bert_squeeze.models.layers',
 'bert_squeeze.utils',
 'bert_squeeze.utils.artifacts',
 'bert_squeeze.utils.callbacks',
 'bert_squeeze.utils.errors',
 'bert_squeeze.utils.losses',
 'bert_squeeze.utils.optimizers',
 'bert_squeeze.utils.schedulers',
 'bert_squeeze.utils.scorers']

package_data = \
{'': ['*'],
 'bert_squeeze.assistants': ['configs/*'],
 'bert_squeeze.data.local_datasets': ['parallel/*']}

install_requires = \
['datasets>=1.8.0,<2.0.0',
 'huggingface-hub==0.13.4',
 'hydra-core>=1.1.1,<2.0.0',
 'lightning>=2.0.0,<3.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'neptune-client[pytorch-lightning]>=0.14.0,<0.15.0',
 'numpy>=1.20.3,<2.0.0',
 'omegaconf>=2.1.0,<3.0.0',
 'overrides>=6.1.0,<7.0.0',
 'psutil>=5.8.0,<6.0.0',
 'python-dotenv>=0.18.0,<0.19.0',
 'scikit-learn>=1.2.2,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'tabulate>=0.8.9,<0.9.0',
 'torch>=2.0.1,<3.0.0',
 'transformers>=4.20.0,<5.0.0']

setup_kwargs = {
    'name': 'bert-squeeze',
    'version': '0.1.0',
    'description': 'Tools for Transformers compression using PyTorch Lightning',
    'long_description': 'None',
    'author': 'JulesBelveze',
    'author_email': 'jules.belveze@hotmail.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)

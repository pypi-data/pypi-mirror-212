# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magma', 'magma_ff', 'magma_ff.commands']

package_data = \
{'': ['*']}

install_requires = \
['dcicutils>=7.5.0,<8.0.0', 'tibanna-ff>=1.3.3,<2.0.0']

entry_points = \
{'console_scripts': ['create-meta-workflow-run = '
                     'magma_ff.commands.create_meta_workflow_run:main',
                     'publish-to-pypi = '
                     'dcicutils.scripts.publish_to_pypi:main']}

setup_kwargs = {
    'name': 'magma-suite',
    'version': '1.5.0.1b17',
    'description': 'Collection of tools to manage meta-workflows automation.',
    'long_description': '# magma\n\n[*Documentation*](https://magma-suite.readthedocs.io/en/latest/ "magma documentation")\n',
    'author': 'Michele Berselli',
    'author_email': 'berselli.michele@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dbmi-bgm/magma',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['polugins']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=6.6.0,<7.0.0', 'polars>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'polugins',
    'version': '0.1.0',
    'description': 'Plugin system for Polars.',
    'long_description': '# Polugins\n\nEarly PoC for a "plugin" system for polars.\n\nNot production ready - barely even alpha ready. Only uploading it now for discussion and to hog the genius package name.\n\nIt\'s meant to solve two issues with using polars API extensions:\n\n- It\'s difficult to ensure that the extensions have been registered in all places in a code where you polars is used.\n\n- Extensions breaks static typing.\n\nThe idea is to describe a single way to expose and collect API extensions - especially for third party packages - \nand then used this discoverbility to also generate type stubs with the added typing from the extensions.\n\nUsers can either call `register_namespaces` themselves or import polars through `polugins.polars` instead.\nLint rules can then be used to enforce that nothing is imported from polars outside of these locations.\n\nThis is still a bit annoying no matter what, unless polars does the import natively.\n\n## Implementation\n\nJust a thin wrapper around `polars.api.register_x_namespace` and then using `importlib.metadata` to collect\nnamespaces from external packages.\n\n## Notes\n\nIt\'s still not entirely clear how an application should register its own namespaces.\nEntry points can be used but\n\n- (1) an application might just want to use its own namespaces and not expose them and \n- (2) its a bit annoying, because changes to entrypoints are only registered when the package is installed, even in editable mode (I think).\n\n\n\n',
    'author': 'StefanBRas',
    'author_email': 'opensource@bruhn.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

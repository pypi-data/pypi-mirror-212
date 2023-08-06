# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prefetch_parser']

package_data = \
{'': ['*']}

install_requires = \
['libscca-python>=20221027,<20221028']

setup_kwargs = {
    'name': 'prefetch-parser',
    'version': '1.0.0',
    'description': '',
    'long_description': "# prefetch-parser\nA parser of Windows prefetch file.\n\nThis repo is strongly inspired from [prefetch2es](https://github.com/sumeshi/prefetch2es), I kept only the part that interest me.\n\n\n\n## Usage\n\n~~~bash\ndacru:~/git/prefetch-parser/ $ python prefetch_parser.py -h\nusage: prefetch_parser.py [-h] [-f PREFETCHFILE] [-o JSONFILE]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -f PREFETCHFILE, --prefetchfile PREFETCHFILE\n                        Windows Prefetch file.\n  -o JSONFILE, --jsonfile JSONFILE\n                        Output json file path. '-' will print command output on terminal.\n~~~\n\n\n\n",
    'author': 'David Cruciani',
    'author_email': 'david.cruciani@circl.lu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DavidCruciani/prefetch_parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

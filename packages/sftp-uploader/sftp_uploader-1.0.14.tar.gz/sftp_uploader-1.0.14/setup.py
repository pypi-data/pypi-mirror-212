# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sftp_uploader',
 'sftp_uploader.applications',
 'sftp_uploader.constants.applications',
 'sftp_uploader.services',
 'sftp_uploader.services.applications',
 'sftp_uploader.services.exceptions']

package_data = \
{'': ['*']}

install_requires = \
['dependency-injector>=4.41.0,<5.0.0',
 'gitpython>=3.1.31,<4.0.0',
 'paramiko>=3.1.0,<4.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0']

entry_points = \
{'console_scripts': ['sftp_setup = sftp_uploader.script_to_setup_package:run']}

setup_kwargs = {
    'name': 'sftp-uploader',
    'version': '1.0.14',
    'description': 'Package for upload data in before commit uncommited files to sftp server',
    'long_description': '# TODO\n\n[ ] Make title, description, which problem is solve, metter of this project description\n\n[ ] Add more [classifiers](https://pypi.org/classifiers/)\n\n[ ] Add tests\n\n[ ] Add additional links to project conf\n\n[ ] Add poetry scripts and pre-commit scripts\n\n[ ] Add poetry post install, if git exists andd to gitignore and setup pre commit hook, and setup config module, if not exists, create and setup it\n',
    'author': 'Moonvent',
    'author_email': 'moonvent@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/moonvent/sftp_uploader/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

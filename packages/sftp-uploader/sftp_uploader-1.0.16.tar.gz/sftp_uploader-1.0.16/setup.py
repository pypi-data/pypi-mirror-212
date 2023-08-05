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
    'version': '1.0.16',
    'description': 'Package for upload data in before commit uncommited files to sftp server',
    'long_description': "# Table of content\n\n0. [What's this, what it's need it?](#what's-this,-what-it's-need-it?) - description of package\n1. [Installation](#installation) - how to install package\n2. [Setup](#setup) - how to setup package\n3. [How script is work](#how-script-is-work) - description of working\n4. [TODO](#todo) - what i need todo in nearby future (task list for me)\n\n# 🧐What's this, what it's need it?\n\nThis script (library) need for upload to sftp before commit files which was changed. It's very comfortable script for me, but if you need it you can use it ! :)\n\n# 📥Installation\n\nWith pip: \n\n`pip install sftp-uploader`\n\nWith poetry:\n\n`poetry add sftp-uploader`\n\n# ⚙️ Setup\n\nFor setup sftp config, you need to execure command `sftp_setup`. After this, you need to input `host`, `port`, `user`, `password` of your sftp server, and after that input a path to remote directory which contain your project,\nfor example: \n\n    Your project in /path/to/my/project\n    Your input `/path/to/my/project` <b>WITHOUT</b> slash in the end (in future a fix it, but now - it's work how it's work), and this directory need to be <b>EXIST</b>\n\nAfter that script add config file to `.gitignore` and add script to load files in `pre-commit` hook file of git. And that's it! Your perfect!!!\n\n<hr>\n\nYou can change in any time config (config name - `sftp_config.json` in root project directory), if you need it, or if any step is broken you can re-execute command and get success result, if\nany step do not need it, script just skip it and all.\n\n# 💪How script is work\n\nScript after you execure command `sftp_setup` ask you a questions about sftp configuration, exactly `host`, `port`, `username`, `password` of sftp connection and after that you remote directory of project root.\nAfter you fill this mini-form, a script create a file `sftp_config.json` which contain all of this information (not encrypted, it's just a `json` format), and with configuration of sftp and filling form is end.\n\nNext step it's create `git` (if not exists) and `gitignore` file (if not exist), after that, script add `sftp_config.json` file to `gitignore` (i think you don't need save your sftp data in your github 😁).\n\nIn the next step, script create or use existed `pre-commit` file, which contain `bash` script which start before you make a commit, you can see a little logs about proccess, how it start, \nwhich files upload which not upload, and after that you can make a commit.\n\n# 🤔TODO\n\n[x] Make title, description, which problem is solve, metter of this project description\n\n[ ] Add more [classifiers](https://pypi.org/classifiers/)\n\n[ ] Add tests\n\n[x] Add additional links to project conf\n\n[x] Add poetry scripts and pre-commit scripts\n\n[x] Add poetry post install, if git exists and to gitignore and setup pre commit hook, and setup config module, if not exists, create and setup it\n",
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

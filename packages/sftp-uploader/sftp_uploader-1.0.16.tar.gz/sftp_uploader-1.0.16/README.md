# Table of content

0. [What's this, what it's need it?](#what's-this,-what-it's-need-it?) - description of package
1. [Installation](#installation) - how to install package
2. [Setup](#setup) - how to setup package
3. [How script is work](#how-script-is-work) - description of working
4. [TODO](#todo) - what i need todo in nearby future (task list for me)

# 🧐What's this, what it's need it?

This script (library) need for upload to sftp before commit files which was changed. It's very comfortable script for me, but if you need it you can use it ! :)

# 📥Installation

With pip: 

`pip install sftp-uploader`

With poetry:

`poetry add sftp-uploader`

# ⚙️ Setup

For setup sftp config, you need to execure command `sftp_setup`. After this, you need to input `host`, `port`, `user`, `password` of your sftp server, and after that input a path to remote directory which contain your project,
for example: 

    Your project in /path/to/my/project
    Your input `/path/to/my/project` <b>WITHOUT</b> slash in the end (in future a fix it, but now - it's work how it's work), and this directory need to be <b>EXIST</b>

After that script add config file to `.gitignore` and add script to load files in `pre-commit` hook file of git. And that's it! Your perfect!!!

<hr>

You can change in any time config (config name - `sftp_config.json` in root project directory), if you need it, or if any step is broken you can re-execute command and get success result, if
any step do not need it, script just skip it and all.

# 💪How script is work

Script after you execure command `sftp_setup` ask you a questions about sftp configuration, exactly `host`, `port`, `username`, `password` of sftp connection and after that you remote directory of project root.
After you fill this mini-form, a script create a file `sftp_config.json` which contain all of this information (not encrypted, it's just a `json` format), and with configuration of sftp and filling form is end.

Next step it's create `git` (if not exists) and `gitignore` file (if not exist), after that, script add `sftp_config.json` file to `gitignore` (i think you don't need save your sftp data in your github 😁).

In the next step, script create or use existed `pre-commit` file, which contain `bash` script which start before you make a commit, you can see a little logs about proccess, how it start, 
which files upload which not upload, and after that you can make a commit.

# 🤔TODO

[x] Make title, description, which problem is solve, metter of this project description

[ ] Add more [classifiers](https://pypi.org/classifiers/)

[ ] Add tests

[x] Add additional links to project conf

[x] Add poetry scripts and pre-commit scripts

[x] Add poetry post install, if git exists and to gitignore and setup pre commit hook, and setup config module, if not exists, create and setup it

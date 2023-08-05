GIT_IGNORE_FILENAME = '.gitignore'

GIT_HOOK_SCRIPT_TO_UPLOAD = """#!/bin/sh

handle_exception() {
    arch -arm64 python -c "import sftp_uploader; sftp_uploader.pre_commit_actions()"
}

trap handle_exception ERR

python -c "import sftp_uploader; sftp_uploader.pre_commit_actions()"

exit 0
"""



GIT_HOOKS_FOLDER = '.git/hooks/'
GIT_HOOK_PRECOMMIT_FILE = f'{GIT_HOOKS_FOLDER}pre-commit'

"""
    Describe what we need to do before commit is complete
"""


from pathlib import Path
from sftp_uploader.services.applications.sftp_uploader import update_files

from sftp_uploader.services.exceptions.pre_commit_actions import CannotActivatePythonVenv


def setup_env():
    activate_this_script = 'venv/bin/activate_this.py'

    if Path(activate_this_script).absolute().exists():
        exec(open(activate_this_script).read(),
             {'__file__': activate_this_script})
    else:
        raise CannotActivatePythonVenv


def pre_commit_actions():
    setup_env()
    update_files()



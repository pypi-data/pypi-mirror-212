"""
    Describe what we need to do before commit is complete
"""


from pathlib import Path
import subprocess
import sys
from sftp_uploader.services.applications.sftp_uploader import update_files

from sftp_uploader.services.exceptions.pre_commit_actions import CannotActivatePythonVenv


def setup_env():

    activate_this_script = 'venv/bin/activate'

    if Path(activate_this_script).absolute().exists():
        activate_script = f"{activate_this_script}"
        command = f"source {activate_script}; {sys.executable}"
        subprocess.run(command, 
                       shell=True,
                       check=True)

    else:
        raise CannotActivatePythonVenv


def pre_commit_actions():
    setup_env()
    update_files()



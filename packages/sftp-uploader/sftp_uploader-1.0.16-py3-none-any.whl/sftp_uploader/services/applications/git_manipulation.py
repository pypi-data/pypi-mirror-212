"""
    All git manipulation logic to git manipulation application here
"""


from dependency_injector.wiring import Provide, inject
from sftp_uploader.applications.dependency_container import DependencyContainer

from sftp_uploader.applications.git_manipulation import CustomGit
from sftp_uploader.constants.applications.env_load import CONFIG_FILE_NAME


@inject
def add_config_file_to_gitignore(git: CustomGit = Provide[DependencyContainer.Git]):
    """
        Add config file package to gitignore
    """
    git.add_to_gitignote(CONFIG_FILE_NAME)


@inject
def add_sftp_upload_in_prehook(git: CustomGit = Provide[DependencyContainer.Git]):
    """
        Add config file package to gitignore
    """
    git.add_prehook_upload()


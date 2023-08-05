"""
    Sftp upload functionality
"""


import os
from os.path import join
from sftp_uploader.applications.env_load import settings
from sftp_uploader.applications.git_manipulation import CustomGit
from sftp_uploader.applications.logs import CustomLogger
from sftp_uploader.applications.sftp import SFTPClient


class SftpUploader:
    """
        Sftp Upload files class

        Attributes:
            __sftp (SFTPClient): sftp client for upload by sftp
            __git (CustomGit): git for getting modified files
    """

    __sftp: SFTPClient = None
    __git: CustomGit = None
    logger: CustomLogger = None

    def __init__(self, 
                 sftp_client: SFTPClient,
                 git_client: CustomGit,
                 logger: CustomLogger
                 ) -> None:
        self.logger = logger
        self.__sftp = sftp_client
        self.__git = git_client
        
    def upload_to_remote(self):
        modified_file_paths: list[str] = self.__git.get_different_files_paths_from_latest_commit()
        self.logger.info(f"Get {len(modified_file_paths)} files to upload")

        for filepath in modified_file_paths:
            self.__sftp.upload_file_to_remote(local_path=filepath,
                                              remote_path=os.path.join(settings.remote_path,
                                                                       filepath))

        self.logger.info('File update complete.')


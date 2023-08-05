"""
    Work with sftp protocol with custom sftp class
"""


import os
from os.path import isdir
from typing import Callable
from sftp_uploader.applications.logs import CustomLogger
from sftp_uploader.applications.ssh import SSHClient
from paramiko import SFTPClient as ParamikoSFTPClient

from sftp_uploader.services.exceptions.sftp import ErrorUploadSFTPException


class SFTPClient:
    """
        Custom sftp client for our needs
    """
    __ssh: SSHClient = None
    __sftp: ParamikoSFTPClient = None
    logger: CustomLogger = None
    __remote_root_path: str = None

    def __init__(self,
                 ssh_client: SSHClient,
                 remote_root_path: str,
                 logger: CustomLogger,
                 ) -> None:
        self.logger = logger
        self.__ssh = ssh_client
        self.__sftp = self.__ssh.get_sftp_client()
        self.__remote_root_path = remote_root_path

    def __del__(self):
        self.__sftp.close()

    def __get_directories_in_path(self, 
                                  path: str):
        """
            Get all directories to file
        """
        directories = []

        while path not in ('', '/'):
            path, directory = os.path.split(path)
            directories.append(directory)

        return directories[::-1]       

    def __check_exist_directory_to_upload(self, 
                                          remote_path: str):
        """
            Check to exists remote directory, if not - create it
        """
        directories = self.__get_directories_in_path(os.path.dirname(remote_path))
        exists_path = ''

        while directories:
            new_path = os.path.join(exists_path, 
                                    directories.pop(0))
            new_remote_path = os.path.join(self.__remote_root_path,
                                           new_path)
            try:
                self.__sftp.stat(new_remote_path)

            except FileNotFoundError:
                self.__sftp.mkdir(new_remote_path)

            finally:
                exists_path = new_path

    def __remove_from_remote(self, 
                             local_path: str,
                             remote_path: str):
        """
            If file was deleted, remove it on remote server
        """
        remove_method: Callable = None

        try:
            self.__sftp.stat(remote_path)

        except Exception as e:
            self.logger.info(f'File `{remote_path}` already delete')

        else:
            if os.path.isdir(local_path):
                remove_method = self.__sftp.rmdir

            else:
                remove_method = self.__sftp.remove

            remove_method(remote_path)
            self.logger.info(f'Success DELETE file `{remote_path}` from remote')

    def __upload_to_remote(self,
                           local_path: str,
                           remote_path: str):
        """
            Upload file to remote
        """
        self.__sftp.put(local_path, 
                        remote_path)
        self.logger.info(f'Success UPLOAD file `{local_path}` to `{remote_path}`')

    def upload_file_to_remote(self,
                              local_path: str,
                              remote_path: str):
        """
            Upload local file to remote server
        """
        self.logger.info(f'Try to modify file `{local_path}` to `{remote_path}`')
        method_to_work_with_sftp: Callable = None

        try:
            self.__check_exist_directory_to_upload(local_path)

            if not os.path.exists(local_path):
                method_to_work_with_sftp = self.__remove_from_remote

            else:
                method_to_work_with_sftp = self.__upload_to_remote

            method_to_work_with_sftp(local_path=local_path,
                                     remote_path=remote_path)

        except Exception as e:
            self.logger.exception(f'In upload to server error - `{e}`\nlocal file - `{local_path}`\nremote file - `{remote_path}`')
            raise ErrorUploadSFTPException



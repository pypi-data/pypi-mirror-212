"""
    Work with ssh connection throught custom SSHClient
"""


from paramiko import SSHClient as ParamikoSSHClient
from paramiko import SFTPClient as ParamikoSFTPClient
from paramiko import AutoAddPolicy
from sftp_uploader.applications.logs import CustomLogger

from sftp_uploader.constants.applications.ssh import AUTH_TIMEOUT
from sftp_uploader.services.exceptions.sftp import ErrorConnectSFTPException
from sftp_uploader.services.exceptions.ssh import ErrorConnectSSHException


class SSHClient:
    """
        Custom class for ssh connection

        Attributes:
            __ssh (paramiko.SSHClient): Main ssh client
    """
    __ssh: ParamikoSSHClient = None
    __sftp: ParamikoSFTPClient= None
    logger: CustomLogger = None

    def __init__(self,
                 host: str,
                 port: int,
                 user: str,
                 password: str,
                 logger: CustomLogger,
                 ) -> None:
        self.logger = logger
        self.__ssh = ParamikoSSHClient()
        self.__ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.__connect_with_ssh(host,
                                port,
                                user,
                                password)

    def __connect_with_ssh(self,
                           host: str,
                           port: int,
                           user: str,
                           password: str,
                           ):
        """
            Function to try connect by ssh
        """
        try:
            self.__ssh.connect(hostname=host, 
                               port=port,
                               username=user,
                               password=password,
                               auth_timeout=AUTH_TIMEOUT)
        except Exception as e:
            self.logger.exception(f'Error in create connection to SSH - `{e}`')
            raise ErrorConnectSSHException

        else:
            self.logger.info('SSH connect open success')

    def __del__(self):
        self.__ssh.close()
        self.logger.info('SSH connect close success')

    def __enter__(self):
        return self

    def __exit__(*args, **kwargs):
        return

    def __open_sftp_client(self) -> ParamikoSFTPClient:
        """
            Open sftp client
        """
        try:
            self.__sftp = self.__ssh.open_sftp()

        except Exception as e:
            self.logger.exception(f'Error in create connection to SFTP - `{e}`')
            raise ErrorConnectSFTPException

        else:
            self.logger.info('SFTP connect open success')

        return self.__sftp

    def get_sftp_client(self) -> ParamikoSFTPClient:
        """
            Get sftp client if exists, in another case create and get it
        """
        return self.__sftp and self.__sftp or self.__open_sftp_client()

    

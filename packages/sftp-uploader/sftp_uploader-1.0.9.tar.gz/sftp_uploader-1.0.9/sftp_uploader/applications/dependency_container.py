"""
    Describe project dependencies classes
"""


from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton 
from sftp_uploader.applications.env_load import settings
from sftp_uploader.applications.git_manipulation import CustomGit
from sftp_uploader.applications.logs import CustomLogger
from sftp_uploader.applications.sftp_uploader import SftpUploader as _SftpUploader

from sftp_uploader.applications.ssh import SSHClient as CustomSSHClient
from sftp_uploader.applications.sftp import SFTPClient as CustomSFTPClient
from sftp_uploader.constants.applications.dependency_container import GIT_CLIENT_LOGGER_NAME, SFTP_CLIENT_LOGGER_NAME, SFTP_UPLOADER_LOGGER_NAME, SSH_CLIENT_LOGGER_NAME



class DependencyContainer(DeclarativeContainer):
    """
        Contaner with all dependencies
    """
    SSHClientLogger = Singleton(CustomLogger,
                                logger_name=SSH_CLIENT_LOGGER_NAME)
    SSHClient = Singleton(CustomSSHClient,
                          host=settings.host,
                          port=settings.port,
                          user=settings.user,
                          password=settings.password,
                          logger=SSHClientLogger,
                          )

    SFTPClientLogger = Singleton(CustomLogger,
                                 logger_name=SFTP_CLIENT_LOGGER_NAME)
    SFTPClient = Singleton(CustomSFTPClient,
                           ssh_client=SSHClient,
                           remote_root_path=settings.remote_path,
                           logger=SFTPClientLogger,
                           )

    GitClientLogger = Singleton(CustomLogger,
                                logger_name=GIT_CLIENT_LOGGER_NAME,
                                )
    Git = Singleton(CustomGit,
                    logger=GitClientLogger,
                    )

    SftpUploaderLogger = Singleton(CustomLogger,
                                   logger_name=SFTP_UPLOADER_LOGGER_NAME,
                                   )
    SftpUploader = Singleton(_SftpUploader,
                             sftp_client=SFTPClient,
                             git_client=Git,
                             logger=SftpUploaderLogger
                             )



from dependency_injector.wiring import Provide, inject

from sftp_uploader.applications.dependency_container import DependencyContainer
from sftp_uploader.applications.sftp_uploader import SftpUploader


@inject
def update_files(sftp_upload: SftpUploader = Provide[DependencyContainer.SftpUploader]):
    sftp_upload.upload_to_remote()



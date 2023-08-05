"""
    Package main sources
"""


from sftp_uploader.applications.dependency_container import DependencyContainer as __DependencyContainer
from sftp_uploader.applications.pre_commit_actions import pre_commit_actions
from sftp_uploader.services.applications import sftp_uploader as __sftp_uploader
from sftp_uploader.services.applications import git_manipulation as __git_manipulation


def init_dependencies():
    """
        Initialize dependency wiring
    """
    dependency_container = __DependencyContainer()
    dependency_container.init_resources()
    dependency_container.wire(modules=[__sftp_uploader,
                                       __git_manipulation])


init_dependencies()


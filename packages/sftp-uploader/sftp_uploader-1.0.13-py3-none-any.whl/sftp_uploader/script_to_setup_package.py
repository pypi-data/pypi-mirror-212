"""
    Poetry post install (as package) commands here
"""


from sftp_uploader.services.applications.git_manipulation import add_config_file_to_gitignore, add_sftp_upload_in_prehook


def run():
    """
        Actions after installing package
    """
    add_config_file_to_gitignore()
    add_sftp_upload_in_prehook()
    

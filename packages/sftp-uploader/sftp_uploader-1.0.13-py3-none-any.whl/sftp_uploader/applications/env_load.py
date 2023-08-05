import os
import json
from pydantic import BaseSettings

from sftp_uploader.constants.applications.env_load import CONFIG_FILE_NAME


class Settings(BaseSettings):
    host: str = None
    port: int = None

    user: str = None
    password: str = None

    remote_path: str = None

    def load_settings(self):
        """
            Load settings if exists, in another case create config file
        """
        if os.path.exists(CONFIG_FILE_NAME):
            self.__load_from_config_file()

        else:
            self.__create_config_file()

    def __load_from_config_file(self):
        """
            Load config from file
        """
        
        self.parse_file(CONFIG_FILE_NAME)

    def __get_config_data_from_user(self) -> tuple[str, str, str, str]:
        """
            Getting data from user
        """
        host = input('Host: ')
        port = input('Port (default=22, press Enter to skip): ')
        if not port:
            port = '22'
        user = input('User: ')
        password = input('Password: ')
        remote_path = input('Remote path from server (project directory, you need to create it and path to it set it here): ')

        return dict(host=host, 
                    port=port, 
                    user=user,
                    password=password,
                    remote_path=remote_path,
                    )

    def __save_config(self, 
                      auth_data: dict):
        """
            Save config file

            TODO:
                * add to gitignore configfile
        """
        with open(CONFIG_FILE_NAME,
                  'w',
                  encoding='utf-8') as config_file:
            json.dump(auth_data, config_file)

    def __create_config_file(self):
        """
            Create config and save it to file
        """
        auth_data: dict = self.__get_config_data_from_user()
        self.__save_config(auth_data=auth_data)

        print(f'Your data is successfully save to file `{CONFIG_FILE_NAME}`, if you want to change it, you can change it here')

        self.parse_file(CONFIG_FILE_NAME)

 
settings = Settings()
settings.load_settings()
settings = Settings.parse_file(CONFIG_FILE_NAME)


import os
import logging


class StartupVariables:
    """
    Grabs variables from environment variables
    """
    @staticmethod
    def __get_key_or_error(key_name: str) -> str:
        """
        Gets a value from env, errors out if value not found
        :param key_name: key name
        :return: key value
        """
        if not (return_value := os.getenv(key_name)):
            logging.error(f"static.env - '{key_name}' key not found. Cannot start API.")
            raise EnvironmentError
        return return_value

    @staticmethod
    def __get_key_or_default(key_name: str, default_value: str):
        """
        Gets a value from env, if env have no value, will return the default value given
        :param key_name: key name
        :param default_value: default value
        :return: key/default value
        """
        if not (return_value := os.getenv(key_name)):
            return_value = default_value
        return return_value

    def __init__(self):
        self.database_uri: str = self.__get_key_or_error("MONGODBURI")
        self.db_name: str = self.__get_key_or_default("DBVERIFYNAME", "honours1")

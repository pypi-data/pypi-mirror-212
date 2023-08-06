"""

"""
# project level libraries
from database.db_creation import DB_Creation
from ip_profile.ip import IP
from phone_data.phone import Phone
from email_data.email import Email


class GraphCE:
    def __init__(self, type_: str, location: str):
        """
        :param type_: type should be IP or PHONE or EMAIL (Uppercase)
        :param location: path of database as a string
        """
        self.__type = type_
        self.__location = f"{location}\\{type_}.sqlite"
        self.database = DB_Creation(self.__location)

        if self.__type == 'IP':
            self.__node_obj = IP(self.__location)
        elif self.__type == 'PHONE':
            self.__node_obj = Phone(self.__location)
        elif self.__type == 'EMAIL':
            self.__node_obj = Email(self.__location)
        else:
            raise TypeError("Invalid type")

    def add(self, value: str, info: dict) -> bool:
        """
        :param value: Phone number or IP address or Email
        :param info: information regarding value as a dict
        :return: True, if element is updated
                 False, if element is not updated
        """
        return self.__node_obj._add(value, info)

    def search(self, value: str) -> bool:
        """

        :param value: Phone number or IP address or Email
        :return: True and info, if element is present
                 False and -1, if element is not present
        """
        return self.__node_obj._is_present(value)

    def update(self, value: str, info: dict) -> bool:
        """

        :param value: Phone number or IP address or Email
        :param info: information regarding value as a dict
        :return: True, if element is updated
                 False, if element is not updated
        """
        return self.__node_obj._update_info(value, info)

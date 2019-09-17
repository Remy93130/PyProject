""" Service who read csv file from the server
the csv will be read with pandas and returns
information needed by the user.
"""


import pandas as pd
import re


class DataService:
    """ The main class for this service, used to manage
    the csv file and extract data.
    Give the csv path in parameter to build the class.
    """
    def __init__(self, data_file):
        """ The class's constructor
        :param data_file: The csv file
        """
        self.data_file = pd.read_csv(data_file)
        self.__format_data()

    def __format_data(self):
        """ Format the data to obtain a readable
        data frame with pandas and manipulate its easier
        """
        regex = r"\[.*\]"
        self.data_file.describe(include="all")

    def get_data_file(self):
        """ Getter for the csv file
        :return:
        """
        return self.data_file

    def get_data_by_country(self, country_name, date=None):
        """
        :param country_name: The name of the country
        :param date: The date from the data (default to None)
        :return: dict
        """
        if country_name:
            return self.data_file
        return None

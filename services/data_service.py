""" Service who read csv file from the server
the csv will be read with pandas and returns
information needed by the user.
"""

import pandas as pd


class DataService:
    """ The main class for this service, used to manage
    the csv file and extract data.
    Give the csv path in parameter to build the class.
    >>> service = DataService('../static/raw_data.csv')
    >>> service.get_data_by_country("Afghanistan", 2017)
    {"Afghanistan": {2017: (10000, 29)}}
    """

    def __init__(self, data_file):
        """ The class's constructor
        :param data_file: The csv file
        """
        self.data_frame = pd.read_csv(data_file)
        self.__format_data()

    def __format_data(self):
        """ Format the data to obtain a readable
        data frame with pandas and manipulate its easier
        """
        self.data_frame["Deaths"].replace(to_replace=r"\[.*\]", value="", regex=True, inplace=True)
        self.data_frame["Deaths_per_100_000_population"].replace(
            to_replace=r"\[.*\]", value="", regex=True, inplace=True)

    def get_data_frame(self):
        """ Getter for the csv file
        :return:
        """
        return self.data_frame

    def get_data_by_country(self, country_name, date=None):
        """
        :param country_name: The name of the country
        :param date: The date from the data (default to None)
        :return: dict
        """
        if country_name:
            return self.data_frame
        return None

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
    {'Afghanistan': {2017: (10000, 29)}}
    >>> service.get_data_by_country("Nambia")

    >>> service.get_data_by_country("Afghanistan")
    {'Afghanistan': {2017: (10000, 29), 2016: (11000, 33), \
2015: (13000, 39), 2014: (14000, 42), 2013: (14000, 43), 2012: (13000, 44), \
2011: (13000, 44), 2010: (12000, 42), 2009: (12000, 44), 2008: (11000, 40), \
2007: (10000, 38), 2006: (11000, 42), 2005: (12000, 46), 2004: (12000, 51), \
2003: (13000, 57), 2002: (12000, 56), 2001: (13000, 62), 2000: (14000, 67)}}
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
        self.data_frame.rename_axis()
        self.data_frame["Deaths"].replace(to_replace=r"\[.*\]", value="", regex=True, inplace=True)
        self.data_frame["Deaths_per_100_000_population"].replace(
            to_replace=r"\[.*\]", value="", regex=True, inplace=True)

    def get_data_frame(self):
        """ Getter for the DataFrame
        :return: The DataFrame
        """
        return self.data_frame

    def get_data_by_country(self, country_name, date=None):
        """ Get information according the country selected and
        the date, if no date provided so the method return all
        data for the country
        :param country_name: The name of the country
        :param date: The date from the data (default to None)
        :return: dict
        """
        country_data = self.data_frame[self.data_frame.Country == country_name]
        if date:
            country_data = country_data[country_data.Year == date]
        if country_data.empty:
            return None
        values = country_data.values.tolist()
        formatted_data = dict()
        formatted_data[country_name] = dict()
        for value in values:
            death_rate = (int(value[2]), int(value[3]))
            formatted_data[country_name][value[1]] = death_rate
        return formatted_data


if __name__ == '__main__':
    import doctest
    doctest.testmod()

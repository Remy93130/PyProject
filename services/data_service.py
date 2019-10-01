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
    >>> service.get_data_by_country("Afghanistan", 3030)

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
        formatted_data = dict()
        formatted_data[country_name] = dict()
        for value in country_data.values.tolist():
            formatted_data[country_name][value[1]] = (int(value[2]), int(value[3]))
        return formatted_data

    def get_data_for_visualisation(self, countries, dates=None):
        """ Prepare the data for visualisation.
        Return a pandas data frames filtered by the list of
        countries and dates passed in arguments. If the
        data frame is empty, return None
        :param countries: The list of countries to select
        :param dates: The list of dates to select
        :return: Pandas data frame or None
        >>> service = DataService('../static/raw_data.csv')
        >>> service.get_data_for_visualisation(["Afghanistan"], [2010, 2011]).shape
        (2, 4)
        >>> service.get_data_for_visualisation(["Afghanistan"], [2010, 2011, 2012]).shape
        (3, 4)
        >>> service.get_data_for_visualisation(["Afghanistan"], [2040])
        """
        country_data = self.data_frame[self.data_frame.Country.isin(countries)]
        if dates:
            country_data = country_data[country_data.Year.isin(dates)]
        return country_data if not country_data.empty else None


if __name__ == '__main__':
    import doctest
    doctest.testmod()

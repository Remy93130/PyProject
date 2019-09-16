"""Service who read csv file from the server
the csv will be read with pandas and returns
information needed by the user.
"""


import pandas as pd


class DataService:
    """The main class for this service, used to manage the csv file and extract data.
    Give the csv path in parameter to build the class.
    """
    def __init__(self, data_file):
        """
        The class's constructor
        :param data_file:
        """
        self.data_file = pd.read_csv(data_file)

    def get_data_by_country(self, country_name):
        return None

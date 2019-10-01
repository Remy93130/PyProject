""" Service for get information about a country
or a region with the restcountries api
"""

import json
import requests

API_URL = "https://restcountries.eu/rest/v2/"


class CountryInfoService:
    """ Main class who contains methods to build
    requests for the API
    """

    def __init__(self):
        """ The class's constructor, use the
        global variable API_URL to get the entry point
        """
        self.api_url = API_URL

    @staticmethod
    def __do_request(url):
        """ Private static method to send the request and
        convert it into a python dict
        :param url: The url to request
        :return: dict
        """
        headers = {"content-type": "application/json"}
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def get_information_by_name(self, country):
        """ Method to obtain data according the country
        given in argument
        :param country: The country selected
        :return: dict or None if the response got 404
        """
        url = self.api_url + "name/" + country
        data = self.__do_request(url)
        if 'status' in data and data['status'] == 404:
            return None
        return data[0]

    def get_information_by_region(self, region):
        """ Method to obtain data according the region
        given in argument
        :param region: The region selected
        :return: dict
        """
        url = self.api_url + "region/" + region
        data = self.__do_request(url)
        return data if 'status' in data and data['status'] == 404 else None

    def complete_data_frame(self, data_frame):
        """ Complete the data frame with information
        who can be found with the countries api and
        return a new data frame
        :param data_frame: The original data frame
        :return: The new data frame with more data
        """
        cached_data = dict()
        rows_to_insert = {rows: [] for rows in ["Code", "Capital", "Population", "Size", "Gini"]}
        for row in data_frame.iterrows():
            frame = row[1]
            if frame.Country not in cached_data:
                cached_data[frame.Country] = self.get_information_by_name(frame.Country)
            rows_to_insert["Code"].append(cached_data[frame.Country]["alpha3Code"])
            rows_to_insert["Capital"].append(cached_data[frame.Country]["capital"])
            rows_to_insert["Population"].append(cached_data[frame.Country]["population"])
            rows_to_insert["Size"].append(cached_data[frame.Country]["area"])
            rows_to_insert["Gini"].append(cached_data[frame.Country]["gini"])
        for column, value in rows_to_insert.items():
            data_frame.insert(len(data_frame.columns), column, value, True)
        return data_frame


if __name__ == '__main__':
    pass

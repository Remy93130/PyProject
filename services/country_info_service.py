""" Service for get information about a country
or a region with the restcountries api
"""

import json
import threading

import requests

API_URL = "https://restcountries.eu/rest/v2/"
NUMBER_THREAD = 5


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
        url = "{}name/{}?fullText=true".format(self.api_url, country)
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
        countries = list()
        threads = list()
        rows_to_insert = {rows: [] for rows in ["Code", "Capital", "Population", "Size", "Gini"]}
        for row in data_frame.iterrows():
            countries.append(row[1].Country)
        split_len = int(len(countries) / NUMBER_THREAD)
        for i in range(NUMBER_THREAD):
            countries_to_find = countries[split_len * i: split_len * (i + 1)]
            thread = threading.Thread(
                target=self.__thread_information,
                args=(countries_to_find, cached_data))
            threads.append(thread)
        threads.append(threading.Thread(
            target=self.__thread_information,
            args=(countries, cached_data)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        for country in countries:
            self.__hydrate_data(rows_to_insert, cached_data, country)
        for column, value in rows_to_insert.items():
            data_frame.insert(len(data_frame.columns), column, value, True)
        self.__add_death_in_percent(data_frame)
        return data_frame

    @staticmethod
    def __add_death_in_percent(data_frame):
        percent_data = list()
        column_name = "Deaths_by_percent_of_population"
        for row in data_frame.iterrows():
            percent_data.append((int(row[1].Deaths) / int(row[1].Population) * 100))
        data_frame.insert(len(data_frame.columns), column_name, percent_data, True)

    @staticmethod
    def __hydrate_data(rows, cached_data, country):
        """ Add the data in the dict
        :param rows: The dict to feed
        :param cached_data: Data get by the API
        :param country: Country selected
        """
        rows["Code"].append(cached_data[country]["alpha3Code"])
        rows["Capital"].append(cached_data[country]["capital"])
        rows["Population"].append(cached_data[country]["population"])
        rows["Size"].append(cached_data[country]["area"])
        rows["Gini"].append(cached_data[country]["gini"])

    def __thread_information(self, countries, data):
        """ Method used by thread to request the API
        :param countries: Countries to fetch
        :param data: dict to feed with the API
        """
        for country in countries:
            if country not in data:
                data[country] = self.get_information_by_name(country)


if __name__ == '__main__':
    pass

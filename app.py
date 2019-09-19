"""Entry point from the application
contains the different controller
and return data needed according to
the user request
"""

import os
from flask import Flask, jsonify
from services.country_info_service import CountryInfoService
from services.data_service import DataService

app = Flask(__name__)


@app.route('/')
def hello_world():
    """A beautiful hello world to test
    the program because you can't bypass it"""
    return jsonify({"message": "Hello World!"})


@app.route('/country/<string:country>')
def test_country_info(country):
    """ Function to test the country API
    :param country: Country to get information
    :return: JSON data about country
    """
    country_info_service = CountryInfoService()
    data = country_info_service.get_information_by_name(country)
    return jsonify(data)


@app.route('/region/<string:region>')
def test_region_info(region):
    """ Function to test the country API
    :param region: Region to get information
    :return: JSON data about region:
    """
    country_info_service = CountryInfoService()
    data = country_info_service.get_information_by_region(region)
    return jsonify(data)


@app.route('/data')
def test_data():
    service = DataService(os.getcwd() + "/static/raw_data.csv")
    return service.get_data_frame().to_string()


if __name__ == '__main__':
    app.run()

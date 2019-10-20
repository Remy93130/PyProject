"""Entry point from the application
contains the different controller
and return data needed according to
the user request
"""

import os
import pathlib
from flask import Flask, jsonify, send_from_directory
from services.country_info_service import CountryInfoService
from services.data_service import DataService
from services.visualisation_service import VisualisationService

app = Flask(__name__, static_url_path="")

CSV_PATH = "./static/raw_data.csv"


@app.route('/')
def hello_world():
    """A beautiful hello world to test
    the program because you can't bypass it"""
    return jsonify({"message": "OK", "status": 200})


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
    """ Function to display data in the csv file
    :return: html tab of the data
    """
    service = DataService(os.getcwd() + CSV_PATH)
    return service.get_data_frame().to_html()


@app.route('/map/<int:date>')
def test_world_map(date):
    """ Function to create a map to the given argument
    Check if the map is not already created else created it
    and return the path to see it
    :param date: The date to visualise data
    :return: JSON data with the relative path
    """
    path = pathlib.Path('resources/map_{}.html'.format(date))
    if not path.exists():
        data_service = DataService(CSV_PATH)
        country_service = CountryInfoService()
        data_frame = data_service.get_data_for_visualisation(dates=[date])
        data_frame = country_service.complete_data_frame(data_frame)
        visualisation = VisualisationService(data_frame)
        file = "./resources/map_{}.html".format(date)
        visualisation.draw_world_map(
            "number of deaths per 100,000 inhabitants in {}".format(date),
            file
        )
    response = dict(path=str(path).replace("\\", "/"))
    return jsonify(response)


@app.route('/resource/<string:path>')
def send_map_file(path):
    """ Route to get maps
    :param path: The html file
    :return: The html file
    """
    return send_from_directory("resources", path)


if __name__ == '__main__':
    app.run(debug=True)

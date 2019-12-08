"""Entry point from the application
contains the different controller
and return data needed according to
the user request
"""

import os
import pathlib
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import cross_origin
from services.country_info_service import CountryInfoService
from services.data_service import DataService
from services.visualisation_service import VisualisationService

app = Flask(__name__, static_url_path="")

CSV_PATH = "/static/raw_data.csv"


@app.route('/countries')
@cross_origin()
def get_countries():
    """ Route to return countries whose we have
    data to display information about
    :return: JSON data with all countries
    """
    data_service = DataService(CSV_PATH)
    data = data_service.get_country_available()
    return jsonify(list(data))


@app.route('/country/<string:country>')
@cross_origin()
def get_country_info(country):
    """ Function to get the country API
    :param country: Country to get information
    :return: JSON data about country
    """
    country_info_service = CountryInfoService()
    data = country_info_service.get_information_by_name(country)
    return jsonify(data)


@app.route('/region/<string:region>')
@cross_origin()
def get_region_info(region):
    """ Function to get the country API
    :param region: Region to get information
    :return: JSON data about region:
    """
    country_info_service = CountryInfoService()
    data = country_info_service.get_information_by_region(region)
    return jsonify(data)


@app.route('/data')
@cross_origin()
def get_data():
    """ Function to display data in the csv file
    :return: html tab of the data
    """
    service = DataService(os.getcwd() + CSV_PATH)
    return service.get_data_frame().to_html()


@app.route('/map/<int:date>')
@cross_origin()
def get_world_map(date):
    """ Function to create a map and a hist to the given argument
    Check if the map is not already created else created both
    map and hist and return the path to see it
    :param date: The date to visualise data
    :return: JSON data with the relative path
    """
    path = pathlib.Path('resources/maps/map_{}.html'.format(date))
    if not path.exists():
        data_service = DataService(CSV_PATH)
        country_service = CountryInfoService()
        data_frame = data_service.prepare_data_for_map_visualisation(dates=[date])
        if data_frame.empty:
            return jsonify(None)
        data_frame = country_service.complete_data_frame(data_frame)
        visualisation = VisualisationService(data_frame)
        file = "./resources/maps/map_{}.html".format(date)
        visualisation.draw_world_map(
            "Number of deaths per 100,000 inhabitants in {}".format(date),
            file
        )
        visualisation.draw_hist_char(
            "Number of deaths as a percentage of the population in {}".format(date),
            "Deaths in percent of population",
            "Number of countries",
            "./resources/maps/hist_{}.html".format(date)
        )
    paths = dict(
        map=(request.host_url + str(path).replace("\\", "/")),
        hist=(request.host_url + str(path).replace("\\", "/").replace('map_', 'hist_'))
    )
    response = dict(paths=paths)
    return jsonify(response)


@app.route('/charts')
@cross_origin()
def get_charts():
    """ Just a route to test the bar charts
    :return: JSON data with the relative path
    """
    data_service = DataService(CSV_PATH)
    countries = request.args.get('countries', default="", type=str)
    countries = countries.split(',')
    countries.sort()
    safe_countries = data_service.get_country_available()
    for country in countries:
        if country not in safe_countries:
            countries.remove(country)
    if not countries or len(countries) > 5:
        return jsonify(None)
    filename = "".join(countries)
    path = pathlib.Path('resources/bars/{}_d.html'.format(filename))
    if not path.exists():
        data = data_service.prepare_data_for_death_chart(countries)
        visualisation = VisualisationService(data)
        file = "./resources/bars/{}".format(filename)
        visualisation.draw_bar_char(
            "Number of deaths over years",
            "Dates",
            "Number of deaths",
            "{}_d.html".format(file)
        )
        DataService.create_cumulative_chart(data)
        visualisation.draw_bar_char(
            "Number of deaths over years (cumulative)",
            "Dates",
            "Number of deaths (cumulative)",
            "{}_c.html".format(file)
        )
    paths = dict(
        death=(request.host_url + str(path).replace("\\", "/")),
        cumulative=(request.host_url + str(path).replace("\\", "/").replace('_d', '_c'))
    )

    response = dict(paths=paths)
    return jsonify(response)


@app.route('/resources/maps/<string:path>')
def send_map_file(path):
    """ Route to get maps
    :param path: The html file
    :return: The html file
    """
    return send_from_directory("resources/maps", path)


@app.route('/resources/bars/<string:path>')
def send_bar_file(path):
    """ Route to get bars chart
    :param path: The html file
    :return: The html file
    """
    return send_from_directory("resources/bars", path)


if __name__ == '__main__':
    app.run()

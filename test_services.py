""" File for test the data frame created by the data service
and test also the completion with the country service.
"""

from services.data_service import DataService
from services.country_info_service import CountryInfoService


def main():
    """Best main ever"""
    data = DataService("static/raw_data.csv")
    info = CountryInfoService()
    data_frame = data.get_data_for_visualisation()
    print("Started data frame :\n--------------------")
    print(data_frame, end="\n\n")
    data = info.complete_data_frame(data_frame)
    print("New data frame :\n----------------")
    print(data)


if __name__ == '__main__':
    main()

from services.data_service import DataService
from services.country_info_service import CountryInfoService
from services.visualisation_service import VisualisationService

data = DataService("./static/raw_data.csv")
info = CountryInfoService()
df = data.get_data_for_visualisation(dates=[2016])
df = info.complete_data_frame(df)
viz = VisualisationService(df)

viz.draw_world_map("map_test", "./resources/map_test.html")

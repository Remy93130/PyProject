""" Service to create different plot and save
them in a folder given by the user
"""


import plotly.graph_objects as go
import plotly.offline as ply


DATES = [i for i in range(2000, 2018)]


class VisualisationService:
    """ Class to provide data visualisation.
    Use the data frame given in constructor
    to build different plot.
    """

    def __init__(self, data):
        self.data = data

    def draw_world_map(self, title, path=""):
        """ Use the data frame in the class to build an
        interactive world map in javascript saved in a
        html file. The file is saved in resources folder
        and return the path to get it
        :param path: The path to save the plot
        :param title: The title to give to the plot
        """
        figure = go.Figure(data=go.Choropleth(
            locations=self.data["Code"],
            z=self.data["Deaths_per_100_000_population"],
            text=self.data["Country"],
            colorscale="hot",
            autocolorscale=False,
            reversescale=True,
            marker_line_color="darkgray",
            marker_line_width=.5,
            colorbar_title="Deaths"
        ))
        figure.update_layout(
            title_text=title,
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type="equirectangular"
            )
        )
        ply.plot(figure, auto_open=False, filename=path)


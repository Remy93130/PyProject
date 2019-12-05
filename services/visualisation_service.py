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

    def draw_bar_char(self, title, x_legend, y_legend, path=""):
        """ Use the data in the object to build a bar chart
        :param title: The chart's title
        :param x_legend: The legend for the X axis
        :param y_legend: The legend for the Y axis
        :param path: The path to save the file
        """
        data = list()
        for country, value in self.data.items():
            data.append(go.Bar(name=country, x=DATES, y=value))
        figure = go.Figure(data=data)
        figure.update_layout(
            barmode="group",
            title_text=title,
            xaxis=dict(
                title=x_legend,
                titlefont_size=16,
                tickfont_size=14
            ),
            yaxis=dict(
                title=y_legend,
                titlefont_size=16,
                tickfont_size=14
            )
        )
        ply.plot(figure, auto_open=False, filename=path)

    def draw_hist_char(self, title, x_legend, y_legend, path=""):
        """ Use the data to build an histogram about death for
        100,000 inhabitants
        :param title: The chart's title
        :param x_legend: The legend for the X axis
        :param y_legend: The legend for the Y axis
        :param path: The path to save the file
        """
        figure = go.Figure()
        figure.add_trace(go.Histogram(
            x=self.data["Deaths_per_100_000_population"],
            xbins=dict(start=0, size=5)
        ))
        figure.update_layout(
            title_text=title,
            xaxis_title_text=x_legend,
            yaxis_title_text=y_legend,
        )
        ply.plot(figure, auto_open=False, filename=path)

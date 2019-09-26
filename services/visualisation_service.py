import plotly.graph_objects as go
import plotly.offline as ply
import pandas as pd


class VisualisationService:
    """"""

    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)

    def draw_world_map(self, title, date):
        pass

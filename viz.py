import plotly.graph_objects as go
import plotly.offline as ply
import pandas as pd

from services.data_service import DataService
from services.country_info_service import CountryInfoService

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

data = DataService("./static/raw_data.csv")
info = CountryInfoService()
df = data.get_data_for_visualisation(dates=[2016])
df = info.complete_data_frame(df)


fig = go.Figure(data=go.Choropleth(
    locations=df['Code'],
    z=df['Deaths'],
    text=df['Country'],
    colorscale='hot',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title='Deaths',
))

fig.update_layout(
    title_text='Death by tuberculosis in 2017',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)

# fig.show()
ply.plot(fig, filename="result.html")

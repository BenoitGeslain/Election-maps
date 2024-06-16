from itertools import chain

from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, MultiPolygons, Plot, WheelZoomTool, PanTool, HoverTool

from utils.maps import *

TOOLTIPS = [
    ("Département", "@departement"),
    ("Circo", "@circo"),
]

plot = Plot(title=None, match_aspect=True)
xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')

yaxis = LinearAxis()
plot.add_layout(yaxis, 'left')
plot.add_tools(WheelZoomTool())
plot.add_tools(PanTool())

plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

for circo in LoadCircoData():
    print(f'{circo["properties"]["nom_reg"]} - {circo["properties"]["nom_dpt"]} - Circo  {circo["properties"]["code_dpt"]}-{circo["properties"]["num_circ"]}')
    # unnested = list(chain(*circo["geometry"]["coordinates"]))
    # print(unnested)
    lonData = []
    latData = []
    for coordinates in circo["geometry"]["coordinates"]:
        try:
            lon, lat = zip(*coordinates)
        except ValueError:
            lon, lat = zip(*list(chain(*coordinates)))

        glyph = MultiPolygons(xs="lon", ys="lat", line_width=1)
        plot.add_glyph(ColumnDataSource(dict(lon=[[[list(lon)]]], lat=[[[list(lat)]]],
                                             departement=[f'{circo["properties"]["nom_dpt"]}'],
                                             circo=[f'{circo["properties"]["code_dpt"]}-{circo["properties"]["num_circ"]}'])),
                                        glyph)

    # break
    # if circo["properties"]["code_dpt"] == "02":
    #     break

plot.add_tools(HoverTool(tooltips=TOOLTIPS))

curdoc().add_root(plot)

show(plot)
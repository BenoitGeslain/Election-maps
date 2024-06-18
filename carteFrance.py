from itertools import chain

from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, MultiPolygons, Plot, WheelZoomTool, PanTool, HoverTool
from bokeh.plotting import output_file

from utils.maps import *
from utils.nfp import *

TOOLTIPS = [
    ("Département", "@departement"),
    ("Circo", "@circo"),
    ("Candidat", "@candidat"),
]

NFPCOLORS = {
    "PS": "hotpink",
    "FI": "red",
    "PCF": "firebrick",
    "PE": "limegreen",
    "-": "dimgrey"
}

NFPData = LoadNFPData()

output_file(filename="output/carte_front_pop.html", title="Front Populaire")
plot = Plot(title=None, width=500, height=500, match_aspect=True)
xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')

yaxis = LinearAxis()
plot.add_layout(yaxis, 'left')
plot.add_tools(WheelZoomTool())
plot.add_tools(PanTool())

plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

for circo in LoadCircoData():
    print(f'{circo["properties"]["nom_reg"]} - {circo["properties"]["nom_dpt"]} - Circo  {circo["properties"]["code_dpt"]}-{int(circo["properties"]["num_circ"]):02d}')
    # unnested = list(chain(*circo["geometry"]["coordinates"]))
    # print(unnested)
    lonData = []
    latData = []
    for coordinates in circo["geometry"]["coordinates"]:
        try:
            lon, lat = zip(*coordinates)
        except ValueError:
            lon, lat = zip(*list(chain(*coordinates)))

        c = f'{circo["properties"]["code_dpt"]}-{int(circo["properties"]["num_circ"]):02d}'
        glyph = MultiPolygons(xs="lon", ys="lat", line_width=0.5, line_color="black", fill_color=NFPCOLORS[NFPData[c]["etiquette"]])
        plot.add_glyph(ColumnDataSource(dict(lon=[[[list(lon)]]], lat=[[[list(lat)]]],
                                             departement=[f'{circo["properties"]["nom_dpt"]}'],
                                             circo=[f'{circo["properties"]["code_dpt"]}-{circo["properties"]["num_circ"]}'],
                                             candidat=[" ".join([NFPData[c]["etiquette"], NFPData[c]["prenom_candidat"], NFPData[c]["nom_candidat"]])])),
                                        glyph)

    # break
    # if circo["properties"]["code_dpt"] == "02":
    #     break

plot.add_tools(HoverTool(tooltips=TOOLTIPS))

curdoc().add_root(plot)

show(plot)
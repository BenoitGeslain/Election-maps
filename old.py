from itertools import chain

from bokeh.layouts import column, row
from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, MultiPolygons, Plot, WheelZoomTool, PanTool, HoverTool, CustomJS, MultiChoice
from bokeh.plotting import output_file, figure

from utils.maps import *
from utils.nfp import *

TOOLTIPS = [
    ("Département", "@departement"),
    ("Circo", "@circo"),
    ("Parti", "@party"),
    ("Candidat", "@candidate"),
    ("Suppléant", "@suppleant"),
]

NFPCOLORS = {
    "PS": "hotpink",
    "FI": "red",
    "PCF": "firebrick",
    "PE": "limegreen",
    "-": "dimgrey"
}

NFPData, NFPParties = LoadNFPData()
CircoData, regions, departements = LoadCircoData()

output_file(filename="output/carte_front_pop.html", title="Front Populaire")
plot = figure(title=None, width=500, height=500, match_aspect=True,
            tools=[PanTool(), WheelZoomTool(), HoverTool(tooltips=TOOLTIPS)])

# multiChoiceParties = MultiChoice(title="Partis", value=NFPParties, options=NFPParties)
multiChoiceRegions = MultiChoice(title="Régions", value=NFPParties, options=NFPParties)
multiChoiceDepartements = MultiChoice(title="Départements", value=departements, options=departements)

for circo in CircoData:
    # print(f'{circo["properties"]["nom_reg"]} - {circo["properties"]["nom_dpt"]} - Circo  {circo["properties"]["code_dpt"]}-{int(circo["properties"]["num_circ"]):02d}')

    # offset = OutreMerOffsets.get(f'{circo["properties"]["code_dpt"]}-{int(circo["properties"]["num_circ"]):02d}', [0, 0])

    lonData = []
    latData = []
    for coordinates in circo["geometry"]["coordinates"]:
        if not circo["properties"]["code_dpt"].isdigit():
            break
        try:
            lon, lat = zip(*coordinates)
        except ValueError:
            lon, lat = zip(*list(chain(*coordinates)))
        # if offset != [0, 0]:
        #     lon = [x + offset[0] for x in lon]
        #     lat = [x + offset[1] for x in lat]
        #     print(lon[0], lat[0])

        c = f'{circo["properties"]["code_dpt"]}-{int(circo["properties"]["num_circ"]):02d}'
        glyph = MultiPolygons(xs="lon", ys="lat", line_width=0.5, line_color="black", fill_color=NFPCOLORS[NFPData[c]["etiquette"]],
                              muted_alpha=0.2, legend_label=NFPData[c]["etiquette"])
        plot.add_glyph(ColumnDataSource(dict(lon=[[[list(lon)]]], lat=[[[list(lat)]]],
                                             departement=[circo["properties"]["nom_dpt"]],
                                             circo=[f'{circo["properties"]["code_dpt"]}-{circo["properties"]["num_circ"]}'],
                                             party=[NFPData[c]["etiquette"]],
                                             candidate=[" ".join([NFPData[c]["prenom_candidat"], NFPData[c]["nom_candidat"]])],
                                             suppleant=[" ".join([NFPData[c]["prenom_suppleant"], NFPData[c]["nom_suppleant"]])])),
                                        glyph)

    # break
    # if circo["properties"]["code_dpt"] == "02":
    #     break

# curdoc().add_root(plot)

show(column(row(multiChoiceRegions, multiChoiceDepartements), plot))
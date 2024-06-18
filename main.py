import json

from bokeh.models import GeoJSONDataSource
from bokeh.plotting import figure, show
from bokeh.models import WheelZoomTool, PanTool, HoverTool

from utils.nfp import *
from utils.maps import *

colors = {
    "PS": "hotpink",
    "FI": "red",
    "PCF": "firebrick",
    "PE": "limegreen",
    "-": "dimgrey"
}

TOOLTIPS = [
    ("Département", "@departement"),
    ("Circo", "@circo"),
    ("Parti", "@party"),
    ("Candidat·e", "@candidate"),
    ("Suppléant·e", "@suppleant"),
]

data = LoadCircoData()
candidates, _ = LoadNFPData()

for i in range(len(data["features"])):
    circo = f'{data["features"][i]["properties"]["code_dpt"]}-{int(data["features"][i]["properties"]["num_circ"]):02d}'
    candidateData = candidates[circo]
    party = candidateData["etiquette"]
    data['features'][i]['properties']['color'] = colors[party]
    data['features'][i]['properties']['party'] = party
    data['features'][i]['properties']['candidate'] = f"{candidateData['prenom_candidat']} {candidateData['nom_candidat']}"
    data['features'][i]['properties']['suppleant'] = f"{candidateData['prenom_suppleant']} {candidateData['nom_suppleant']}"
    data['features'][i]['properties']['region'] = data["features"][i]["properties"]["code_reg"]
    data['features'][i]['properties']['departement'] = data["features"][i]["properties"]["code_dpt"]
    data['features'][i]['properties']['circo'] = circo

geo_source = GeoJSONDataSource(geojson=json.dumps(data))

p = figure(background_fill_color="white", width=500, height=500, match_aspect=True,
            x_range=(-7, 11), y_range=(40, 54),
            tools=[PanTool(), WheelZoomTool(), HoverTool(tooltips=TOOLTIPS)])

p.patches('xs', 'ys', source=geo_source, line_width=1, line_color="light_grey", fill_color='color')

show(p)
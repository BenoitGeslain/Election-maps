import json

from bokeh.layouts import column
from bokeh.models import GeoJSONDataSource, WheelZoomTool, PanTool, HoverTool, MultiChoice, AutocompleteInput, CustomJS
from bokeh.plotting import figure, show, output_file

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

data, regions, departements = LoadCircoData()
candidates, NFPParties = LoadNFPData()

multiChoiceParties = MultiChoice(title="Partis", value=NFPParties, options=NFPParties)
multiChoiceParties.js_on_change("value", CustomJS(code="""
    console.log('multiChoiceParties: value=' + this.value, this.toString())
"""))
autoCompleteRegions =  AutocompleteInput(title="Régions:", completions=regions, case_sensitive=False, min_characters=1, search_strategy="includes", restrict=True)
autoCompleteRegions.js_on_change("value", CustomJS(code="""
    console.log('multiChoiceParties: value=' + this.value, this.toString())
"""))
autoCompleteDepartements =  AutocompleteInput(title="Département:", completions=departements, case_sensitive=False, search_strategy="includes")
autoCompleteDepartements.js_on_change("value", CustomJS(code="""
    console.log('multiChoiceParties: value=' + this.toString())
"""))

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

output_file(filename="output/input.html", title="Front Populaire")
p = figure(background_fill_color="white", width=500, height=500, match_aspect=True,
            x_range=(-7, 11), y_range=(40, 54),
            tools=[PanTool(), WheelZoomTool(), HoverTool(tooltips=TOOLTIPS)])

p.axis.visible = False

p.patches('xs', 'ys', source=geo_source, line_width=1, line_color="light_grey", fill_color='color')

show(column(multiChoiceParties, autoCompleteRegions, autoCompleteDepartements, p))

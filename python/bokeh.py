import json

from bokeh.layouts import column
from bokeh.models import GeoJSONDataSource, WheelZoomTool, PanTool, HoverTool, MultiChoice, AutocompleteInput, CustomJS, Range1d
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
    ("Région", "@region"),
    ("Département", "@departement"),
    ("Circo", "@circo"),
    ("Parti", "@party"),
    ("Candidat·e", "@candidate"),
    ("Suppléant·e", "@suppleant"),
]

data, regions, departements = LoadCircoData()
regionData = LoadRegionData()
departementData = LoadDepartementData()
candidates, NFPParties = LoadNFPData()


# Filtering tool. TODO make them work with JS
multiChoiceParties = MultiChoice(title="Partis", value=NFPParties, options=NFPParties)
multiChoiceParties.js_on_change("value", CustomJS(code="""
    console.log('multiChoiceParties: value=' + this.value, this.toString())
"""))
autoCompleteRegions =  AutocompleteInput(title="Région:", completions=regions, case_sensitive=False, min_characters=1, search_strategy="includes", restrict=True)
autoCompleteRegions.js_on_change("value", CustomJS(code="""
    console.log('multiChoiceParties: value=' + this.value, this.toString())
"""))
autoCompleteDepartements =  AutocompleteInput(title="Département:", completions=departements, case_sensitive=False, search_strategy="includes")
autoCompleteDepartements.js_on_change("value", CustomJS(code="""
    console.log('multiChoiceParties: value=' + this.value, this.toString())
"""))

# populating tooltip fields
for i in range(len(data["features"])):
    circo = f'{data["features"][i]["properties"]["code_dpt"]}-{int(data["features"][i]["properties"]["num_circ"]):02d}'
    candidateData = candidates[circo]
    party = candidateData["etiquette"]
    data['features'][i]['properties']['color'] = colors[party]
    data['features'][i]['properties']['party'] = party
    data['features'][i]['properties']['candidate'] = f"{candidateData['prenom_candidat']} {candidateData['nom_candidat']}"
    data['features'][i]['properties']['suppleant'] = f"{candidateData['prenom_suppleant']} {candidateData['nom_suppleant']}"
    data['features'][i]['properties']['region'] = data["features"][i]["properties"]["nom_reg"]
    data['features'][i]['properties']['departement'] = data["features"][i]["properties"]["nom_dpt"]
    data['features'][i]['properties']['circo'] = f'{data["features"][i]["properties"]["num_circ"]}'

# converting data to Bokeh GeoJSON format
geoSource = GeoJSONDataSource(geojson=json.dumps(data))
geoRegionSource = GeoJSONDataSource(geojson=json.dumps(regionData))
geoDepartementSource = GeoJSONDataSource(geojson=json.dumps(departementData))

output_file(filename="output/index.html", title="Front Populaire")
hoverTool = HoverTool(tooltips=TOOLTIPS)

p = figure(background_fill_color="gainsboro", width=1000, height=1000, match_aspect=True,
            x_range=Range1d(-7, 11, bounds=(-7.5, 11.5)), y_range=Range1d(40, 54, bounds=(39.5, 54.5)), # Setting plot initial range and max range
            tools=[PanTool(), WheelZoomTool(), hoverTool])

circoPatches = p.patches('xs', 'ys', source=geoSource, line_width=0.5, line_color="white", fill_color='color')
p.patches('xs', 'ys', source=geoDepartementSource, line_width=1, line_color="white", fill_alpha=0)
# p.patches('xs', 'ys', source=geoRegionSource, line_width=1.5, line_color="white", fill_alpha=0)

hoverTool.renderers = [circoPatches]

p.axis.visible = False
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

show(column(multiChoiceParties, autoCompleteRegions, autoCompleteDepartements, p))
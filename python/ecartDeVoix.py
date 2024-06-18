from mergeCSVToGeoJson import *

geoData = LoadGeoData()
legis2022Data = Loadlegis2022Data()

for circo in geoData['features']:
    circoId = f'{circo["properties"]["code_dpt"]}{int(circo["properties"]["num_circ"]):02d}'

    try:
        for header in legis2022Data[circoId].keys():
            circo["properties"][header] = legis2022Data[circoId][header]
    except KeyError:
        pass

with open('output/legis2022.json', 'w') as f:
    json.dump(geoData, f)

from mergeCSVToGeoJson import *

labels = {
    "nom_reg": "Région",
    "nom_dpt": "Département",
}

def changePropertyLables(data, labels):
    for circo in geoData['features']:
        for property in labels:
            if property in circo["properties"].keys():
                circo["properties"][labels[property]] = circo["properties"][property]
                circo["properties"].pop(property)
    return data

geoData = LoadGeoData()
legis2022Data = Loadlegis2022Data()

for circo in geoData['features']:
    circoId = f'{circo["properties"]["code_dpt"]}{int(circo["properties"]["num_circ"]):02d}'

    try:
        for header in legis2022Data[circoId].keys():
            circo["properties"][header] = legis2022Data[circoId][header]
    except KeyError:
        pass

geoData = changePropertyLables(geoData, labels)

with open('output/legis2022.json', 'w') as f:
    json.dump(geoData, f)

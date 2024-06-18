import json

# OutreMerOffsets = {
#     "ZA-01": [77, 34],
#     "ZA-02": [77, 34],
#     "ZA-03": [77, 34],
#     "ZA-04": [77, 34],
#     "ZB-01": [77, 34],
#     "ZB-02": [77, 34],
#     "ZB-03": [77, 34],
#     "ZB-04": [77, 34],
#     "ZC-01": [72, 46],
#     "ZC-02": [72, 46],
#     "ZD-01": [-40, 68],
#     "ZD-02": [-40, 68],
#     "ZD-03": [-40, 68],
#     "ZD-04": [-40, 68],
#     "ZD-05": [-40, 68],
#     "ZD-06": [-40, 68],
#     "ZD-07": [-40, 68],
#     "ZN-01": [-148, 63],
#     "ZN-02": [-148, 63],
#     "ZN-03": [-148, 63],
#     "ZP-01": [182, 63],
#     "ZP-02": [182, 63],
#     "ZP-03": [182, 63],

#     "ZX-01": [0, 0],
#     "ZW-01": [0, 0],
# }

def LoadCircoData():
    data = []
    regions = []
    departements = []
    with open('data/france-circonscriptions-legislatives-2012.json', encoding="utf8") as f:
        data = json.load(f)

        data['features'] = [circo for circo in data['features'] if circo['properties']['code_reg'].isdigit() and int(circo['properties']['code_reg'])<96]
        for circo in data['features']:
            if not circo["properties"]["nom_reg"] in regions:
                regions.append(circo["properties"]["nom_reg"])
            if not circo["properties"]["nom_dpt"] in departements:
                departements.append(circo["properties"]["nom_dpt"])
        return data, regions, departements

def LoadRegionData():
    data = []
    with open('data/regions-france.json', encoding="utf8") as f:
        data = json.load(f)

        return data

def LoadDepartementData():
    data = []
    with open('data/departements-france.json', encoding="utf8") as f:
        data = json.load(f)

        return data
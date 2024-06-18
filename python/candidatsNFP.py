import json
from mergeCSVToGeoJson import LoadGeoData, LoadCandidateData

geoData = LoadGeoData()
candidateData = LoadCandidateData()

for circo in geoData['features']:
    circoId = f'{circo["properties"]["code_dpt"]}{int(circo["properties"]["num_circ"]):02d}'

    try:
        for header in candidateData[circoId].keys():
            circo["properties"][header] = candidateData[circoId][header]
    except KeyError:
        pass

with open('output/candidates.json', 'w') as f:
    json.dump(geoData, f)

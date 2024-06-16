import json

def LoadCircoData():
    data = []
    with open('data/france-circonscriptions-legislatives-2012.json') as f:
        d = json.load(f)

        data = d["features"]
        return data


        # for circo in data:
        #     coordinates = circo["geometry"]["coordinates"]
        #     print(coordinates)
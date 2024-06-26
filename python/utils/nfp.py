import csv

def LoadNFPData():
    with open('data\candidatures-front-populaire-et-dissidents.csv', encoding="utf8") as f:
        data = csv.DictReader(f, delimiter=',')
        dataParsed = {}
        parties = []
        for row in data:
            dataParsed[row['circonscription']] = row
            dataParsed[row['circonscription']].pop("circonscription")
            if not row["etiquette"] in parties:
                parties.append(row["etiquette"])
        return dataParsed, parties

import csv

def LoadNFPData():
    with open('data\candidatures-front-populaire-et-dissidents.csv', encoding="utf8") as f:
        data = csv.DictReader(f, delimiter=',')
        print(data.fieldnames)
        dataParsed = {}
        for row in data:
            print(row)
            dataParsed[row['circonscription']] = row
            dataParsed[row['circonscription']].pop("circonscription")
        return dataParsed
print(LoadNFPData())
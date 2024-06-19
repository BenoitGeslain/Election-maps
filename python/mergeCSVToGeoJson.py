import json, csv

def LoadGeoData():
    data = []
    with open('data/france-circonscriptions-legislatives-2012.json', encoding="utf8") as f:
        data = json.load(f)
        return data

def LoadCandidateData():
    with open('data\candidatures-legislatives2024-t1.csv', encoding="utf8") as f:
        dataParsed = {}
        data = csv.DictReader(f, delimiter=',')
        for row in data:
            if row["codeNuance"] == "UG":
                circoId = row['circonscription']
                row.pop("circonscription")
                dataParsed[circoId] = row
        return dataParsed

def Loadlegis2022Data():
    with open('data\legislative2022_t2_par_circo.csv', encoding="utf8") as f:
        dataParsed = {}
        data = csv.DictReader(f, delimiter=';')
        for row in data:
            circo = f'{row["Code du département"]}{row["Code de la circonscription"]}'
            idNFP = 0
            idVS = 0
            if row["Nuance1"] in ["NUP", "ECO", "DVG"]:
                idNFP = 1
                idVS = 2
            elif row["Nuance2"] in ["NUP", "ECO", "DVG"]:
                idNFP = 2
                idVS = 1
            elif "Nuance3" in row.keys() and row["Nuance3"] in ["NUP", "ECO", "DVG"]:
                idNFP = 3
                idVS = 1
            # print(circo, idNFP, idVS)

            if idNFP == 0 or row[f"Voix{idVS}"] == None:
                with open('data\legislative2022_t1_par_circo.csv', encoding="utf8") as f:
                    dataT1 = csv.DictReader(f, delimiter=';')

                    voix = 0
                    voixVs = 0
                    candidatNupes = ""
                    elu = ""
                    for rowT1 in dataT1:
                        if f'{rowT1["Code du département"]}{rowT1["Code de la circonscription"]}' == circo:
                            for i in range(30):
                                if (not f"Nom{i}" in rowT1.keys()) or rowT1[f"Nom{i}"] == None:
                                    break
                                if rowT1[f"Nuance{i}"] in ["NUP", "ECO", "DVG"]:
                                    if rowT1[f"Nuance{i}"] == "NUP":
                                        candidatNupes = f'{rowT1[f"Prénom{i}"]} {rowT1[f"Nom{i}"]}'
                                    voix += int(rowT1[f"Voix{i}"])
                                else:
                                    if int(rowT1[f"Voix{i}"]) > voixVs:
                                        voixVs = int(rowT1[f"Voix{i}"])
                                if rowT1[f"Sièges{i}"] == "Elu":
                                    elu = f'{rowT1[f"Prénom{i}"]} {rowT1[f"Nom{i}"]} {rowT1[f"Nuance{i}"]}'
                            dataParsed[circo] = {"Circonscription": circo,
                                                "Tour": 1,
                                                "Candidat NUPES ou Dissident de gauche": candidatNupes,
                                                "Contre": "",
                                                "Elu": elu,
                                                "Gagné": "Oui" if (voix > voixVs) else "Non",
                                                "Ecart de voix": voix - voixVs,
                                                "Ecart de voix (valeur absolue)": abs(voix - voixVs)
                            }

                            break
            else:
                contre = ""
                elu = ""
                for i in range(1, 5):
                    if not row[f"Nuance{i}"] in ["NUP", "ECO", "DVG"] and row[f"Prénom{i}"] != None:
                        contre += f'{row[f"Prénom{i}"]} {row[f"Nom{i}"]} {row[f"Nuance{i}"]}' + ', '
                    if row[f"Sièges{i}"] == "Elu":
                        elu = f'{row[f"Prénom{i}"]} {row[f"Nom{i}"]} {row[f"Nuance{i}"]}'
                dataParsed[circo] = {"Circonscription": circo,
                                    "Tour": 2,
                                    "Candidat NUPES ou Dissident de gauche": f'{row[f"Prénom{idNFP}"]} {row[f"Nom{idNFP}"]}',
                                    "Contre": contre,
                                    "Elu": elu,
                                    "Gagné": "Oui" if (int(row[f"Voix{idNFP}"]) > int(row[f"Voix{idVS}"])) else "Non",
                                    "Ecart de voix": int(row[f"Voix{idNFP}"]) - int(row[f"Voix{idVS}"]),
                                    "Ecart de voix (valeur absolue)": abs(int(row[f"Voix{idNFP}"]) - int(row[f"Voix{idVS}"]))
                }
        with open('data\legislative2022_t1_par_circo.csv', encoding="utf8") as f:
            dataT1 = csv.DictReader(f, delimiter=';')
            voix = 0
            voixVs = 0
            candidatNupes = ""
            elu = ""
            for rowT1 in dataT1:
                if "Elu" in rowT1.values():
                    circo = f'{rowT1["Code du département"]}{rowT1["Code de la circonscription"]}'
                    for i in range(30):
                        if (not f"Nom{i}" in rowT1.keys()) or rowT1[f"Nom{i}"] == None:
                            break
                        if rowT1[f"Nuance{i}"] in ["NUP", "ECO", "DVG"]:
                            if rowT1[f"Nuance{i}"] == "NUP":
                                candidatNupes = f'{rowT1[f"Prénom{i}"]} {rowT1[f"Nom{i}"]}'
                            voix += int(rowT1[f"Voix{i}"])
                        else:
                            if int(rowT1[f"Voix{i}"]) > voixVs:
                                voixVs = int(rowT1[f"Voix{i}"])
                        if rowT1[f"Sièges{i}"] == "Elu":
                            elu = f'{rowT1[f"Prénom{i}"]} {rowT1[f"Nom{i}"]} {rowT1[f"Nuance{i}"]}'
                    dataParsed[circo] = {"Circonscription": circo,
                                        "Tour": 1,
                                        "Candidat NUPES ou Dissident de gauche": candidatNupes,
                                        "Contre": "",
                                        "Elu": elu,
                                        "Gagné": "Oui" if (voix > voixVs) else "Non",
                                        "Ecart de voix": voix - voixVs,
                                        "Ecart de voix (valeur absolue)": abs(voix - voixVs)
                    }
        return dataParsed
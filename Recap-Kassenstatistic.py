import os
import numpy as np
import matplotlib.pyplot as plt


# Funktion zum Einlesen der Daten aus einer Textdatei in ein NumPy-Strukturiertes Array
def einlesen_und_konvertieren(datei_name):
    daten = []
    with open(datei_name, "r") as file:
        next(file)  # Überspringe die erste Zeile
        for zeile in file:
            uhrzeit, einkaufswert = zeile.strip().split()
            daten.append((uhrzeit, float(einkaufswert)))

    dtype = np.dtype([("Uhrzeit", "U5"), ("Einkaufswert", "f8")])
    return np.array(daten, dtype=dtype)


# Dictionäre verwenden, um die Strukturierten Arrays basierend auf Filialnamen zu speichern
filialen = {}
verzeichnis = "dateien/kasse"

# Durchsuchen Sie das Verzeichnis nach Dateien
for datei_name in os.listdir(verzeichnis):
    if datei_name.endswith(".txt"):
        dateiname, _ = os.path.splitext(datei_name)
        filialname = dateiname.split("_")[0]
        datei_pfad = os.path.join(verzeichnis, datei_name)

        if filialname not in filialen:
            filialen[filialname] = einlesen_und_konvertieren(datei_pfad)
        else:
            # Wenn der Filialname bereits im Dictionary vorhanden ist, fügen Sie die Daten zusammen
            filialen[filialname] = np.concatenate(
                [filialen[filialname], einlesen_und_konvertieren(datei_pfad)]
            )

# Ausgabe der kombinierten Strukturierten Arrays
for filialname, daten in filialen.items():
    # Maximaler Einkauf
    max_einkauf = np.max(daten["Einkaufswert"])
    min_einkauf = np.min(daten["Einkaufswert"])
    # Durchschnittseinkauf
    durchschnittseinkauf = np.average(daten["Einkaufswert"])

    # Durchschnittseinkauf pro Stunde
    # Annahme: Die Uhrzeit ist im Format "hh:mm"
    uhrzeiten = [
        uhrzeit.split(":")[0] for uhrzeit in daten["Uhrzeit"]
    ]  # merken welche Uhrzeiten wir haben
    stunden = list(range(8, 20))  # Öffnungszeiten von 8:00 bis 20:00 Uhr
    durchschnittseinkauf_pro_stunde = []

    for stunde in stunden:
        stunden_einkauf = []
        for i, uhr in enumerate(
            uhrzeiten
        ):  # für jede Uhrzeit in unseren Daten prüfen wir ob ein Einkauf vorhanden ist
            if int(uhr) == stunde:
                stunden_einkauf.append(daten["Einkaufswert"][i])

        print(stunden_einkauf)
        if stunden_einkauf:  # wenn in der Stunde etwas gekauft wurde
            durchschnitt = np.average(stunden_einkauf)
        else:
            durchschnitt = 0
        # Erzeugen einer Tupel für stunde, durchschitt und diese in den durchschnittseinkauf_pro_stunde liste setzten
        durchschnittseinkauf_pro_stunde.append((stunde, durchschnitt))

    # Ausgabe pro Filiale
    print(f"Filiale: {filialname} | Anzahl Sätze: {daten.shape[0]}")
    print(f"Maximaler Einkauf: {max_einkauf}")
    print(f"Minimaler Einkauf: {min_einkauf}")
    print(f"Durchschnittseinkauf: {durchschnittseinkauf}")
    print(f"Durchschnittseinkauf pro Stunde: {durchschnittseinkauf_pro_stunde}")

    if filialname == "filiale1":
        maximaler_einkauf_filiale1 = max_einkauf
        minimaler_einkauf_filiale1 = min_einkauf
        DurchschnittseinkaufproStunde_filiale1 = [
            datensatz[1] for datensatz in durchschnittseinkauf_pro_stunde
        ]

    else:
        maximaler_einkauf_filiale2 = max_einkauf
        minimaler_einkauf_filiale2 = min_einkauf
        DurchschnittseinkaufproStunde_filiale2 = [
            datensatz[1] for datensatz in durchschnittseinkauf_pro_stunde
        ]

maxeinkauf = [maximaler_einkauf_filiale1, maximaler_einkauf_filiale2]
mineinkauf = [minimaler_einkauf_filiale1, minimaler_einkauf_filiale2]


x_pos = np.arange(len(filialen))
bar_width = 0.9
plt.subplot(2, 2, 1)
plt.bar(x_pos, maxeinkauf, color="blue")
plt.xticks(x_pos, filialen)
plt.yticks()
plt.xlabel("Filialen")
plt.ylabel("Maximaler Einkauf")
plt.title("Maximaler Einkauf pro Filiale")

x_pos2 = np.arange(len(filialen))
bar_width = 0.9
plt.subplot(2, 2, 2)
plt.bar(x_pos2, mineinkauf, color="red")
plt.xticks(x_pos, filialen)
plt.yticks()
plt.xlabel("Filialen")
plt.ylabel("Minimaler Einkauf")
plt.title("Minimaler Einkauf pro Filiale")

print("Hi", DurchschnittseinkaufproStunde_filiale1)
print("stunden", stunden)


bar_width = 0.9
plt.subplot(2, 2, 3)
plt.plot(
    stunden,
    DurchschnittseinkaufproStunde_filiale1,
    stunden,
    DurchschnittseinkaufproStunde_filiale1,
    "oy",
    stunden,
    DurchschnittseinkaufproStunde_filiale2,
    stunden,
    DurchschnittseinkaufproStunde_filiale2,
    "or",
)
plt.xlabel("Stunde")
plt.ylabel("Durchschnitts Einkauf pro Stunde")
plt.title("Durchschnitts Einkauf pro Stunde pro Filiale")


plt.show()

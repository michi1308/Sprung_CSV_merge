import csv
import os

# Direkten Pfad zu den Daten angeben
data_root = r"M:\Rohdaten\Sprung\BIA_Norm\DepthJump\3D\LESS_Landing"  # mit r davor
# Erhalte die Dateinamen im angegebenen Verzeichnis
filenames = os.listdir(data_root)

# Leere Liste als Platzhalter für die neue Datei
all_data = []

# Für die Länge der Liste mach bitte Folgendes:
for file in filenames:
    uebergabe = os.path.join(data_root, file)  # Kreiere den aktuellen Pfad
    with open(uebergabe, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        raw_data = list(csv_reader)

        # Prüfen, ob die Datei genug Zeilen hat
        if len(raw_data) >= 6:
            data_without_header = raw_data[5]  # 6. Zeile (Index 5)
            all_data.append(data_without_header)  # Zeile zur Liste hinzufügen

# Speicherdestination angeben
output_path = r"M:\Rohdaten\Sprung\BIA_Norm\DepthJump\3D\LESS_Landing\output.csv"  # r davor, Dateiname notwendig

# Überprüfen, ob die Datei bereits existiert
if os.path.isfile(output_path):
    print(f"ATTENTION: File with path {output_path} already exists. \n"
          "Please save this file in another directory.")
else:
    with open(output_path, 'w', newline='') as output_csvfile:
        writer = csv.writer(output_csvfile)
        writer.writerows(all_data)  # Schreibe die gesammelten Zeilen in die neue Datei
        print("ALL DONE! Your file is ready to view :)")



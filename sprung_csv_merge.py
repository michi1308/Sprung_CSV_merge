import csv
import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Funktion zur Verarbeitung der CSV-Dateien
def csv_daten_verarbeiten(data_root):
    """Liest alle CSV-Dateien im angegebenen Verzeichnis und extrahiert die 6. Zeile jeder Datei,
       wobei die Daten in Spalten aufgeteilt werden."""
    filenames = os.listdir(data_root)
    all_data = []

    # Durchlaufe alle Dateien im Verzeichnis
    for file in filenames:
        uebergabe = os.path.join(data_root, file)  # Pfad zur Datei erstellen

        try:
            with open(uebergabe, 'r', newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter='\t')  # Tabulator als Trenner
                raw_data = list(csv_reader)

                # Prüfen, ob die Datei genug Zeilen hat
                if len(raw_data) >= 6:
                    data_without_header = raw_data[5]  # 6. Zeile (Index 5) extrahieren
                    all_data.append(data_without_header)  # Ganze Zeile zur Liste hinzufügen
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen der Datei {file}: {e}")
            continue  # Überspringe diese Datei und fahre mit der nächsten fort

    # Rückgabe als DataFrame
    return pd.DataFrame(all_data)

# Funktion zur Umwandlung von Punkt zu Komma in den Zahlen
def konvertiere_zahlen_von_punkt_zu_komma(data):
    """Konvertiert Dezimalzahlen von Punkt zu Komma."""
    if data is None:
        return None

    def punkt_zu_komma(value):
        """Hilfsfunktion zum Ersetzen von Punkt durch Komma."""
        value_str = str(value).replace('.', ',')
        try:
            return float(value_str.replace(',', '.'))
        except ValueError:
            return value_str

    # Wende die Umwandlung auf alle Spalten an
    for spalte in data.columns:
        data[spalte] = data[spalte].map(punkt_zu_komma)

    return data

# Funktion zum Lesen einer Excel-Vorlage
def hole_vorlage(file_path, num_rows=5):
    """Liest die ersten `num_rows` Zeilen einer Excel-Vorlage."""
    try:
        template_df = pd.read_excel(file_path, header=None)
        return template_df.head(num_rows)
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Lesen der Vorlage: {e}")
        return None

# Funktion zum Speichern der Daten in einer Excel-Datei
# def daten_speichern(data, output_path):
#     """Speichert die Daten in einer Excel-Datei."""
#     if data is None:
#         print("Keine Daten zum Speichern.")
#         return
#     try:
#         data.to_excel(output_path, index=False, header=False)
#         print(f'Datei erfolgreich gespeichert als {output_path}')
#     except Exception as e:
#         messagebox.showerror("Fehler", f"Fehler beim Speichern der Excel-Datei: {e}")

def daten_speichern(data, output_path):
    """Speichert die Daten in einer Excel-Datei."""
    if data is None:
        print("Keine Daten zum Speichern.")
        return
    try:
        data.to_excel(output_path, index=False, header=False)
        print(f'Datei erfolgreich gespeichert als {output_path}')
        # Erfolgs-Meldung anzeigen
        messagebox.showinfo("Erfolg", f"Die Datei wurde erfolgreich gespeichert unter: {output_path}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Speichern der Excel-Datei: {e}")

# Funktion, die beim Klicken des Buttons ausgeführt wird
def button_klick(path_entry, vorlage_entry):
    """Verarbeitet CSV-Daten und speichert sie in einer Excel-Datei."""
    data_root = path_entry.get()  # Pfad für CSV-Daten
    vorlage_file = vorlage_entry.get()  # Pfad zur Excel-Vorlage

    # Überprüfen, ob der Pfad existiert
    if not os.path.isdir(data_root):
        messagebox.showerror("Fehler", "Der angegebene Pfad existiert nicht!")
        return

    # Verarbeite die CSV-Daten
    all_data = csv_daten_verarbeiten(data_root)

    # Konvertiere die Dezimalstellen in den Daten (Punkt zu Komma)
    data_with_comma = konvertiere_zahlen_von_punkt_zu_komma(all_data)

    # Hole die Vorlage und füge sie oben an
    template_data = hole_vorlage(vorlage_file)
    if template_data is not None:
        combined_data = pd.concat([template_data, data_with_comma], ignore_index=True)
    else:
        combined_data = data_with_comma

    # Speicherpfad und Speichern der Datei
    output_path = os.path.join(data_root, "output_csv.xlsx")
    daten_speichern(combined_data, output_path)

# GUI erstellen
def gui_erstellen():
    """Erstellt die GUI mit tkinter."""
    root = tk.Tk()
    root.title("CSV Verarbeitungs-Tool")
    root.geometry("700x300")

    # Info-Label für die Pfad-Eingabe
    info_label = tk.Label(root, text="Pfade immer ohne Anführungsstriche angeben.")
    info_label.pack(padx=15, pady=5)

    # Eingabe für den CSV-Ordnerpfad
    path_label = tk.Label(root, text="Hier den Ordnerpfad zu den CSV-Daten angeben. Die fertige Datei wird in den Ordner gespeichert.")
    path_label.pack(padx=15, pady=5)
    path_entry = tk.Entry(root, width=85)
    path_entry.pack(padx=15, pady=5)

    # Eingabe für den Vorlagenpfad
    vorlage_label = tk.Label(root, text="Hier den Pfad zur Excel-Vorlage angeben.")
    vorlage_label.pack(padx=15, pady=5)
    vorlage_entry = tk.Entry(root, width=85)
    vorlage_entry.pack(padx=15, pady=5)

    # Button zum Starten des Verarbeitungsprozesses
    process_button = tk.Button(root, text="Verarbeiten", command=lambda: button_klick(path_entry, vorlage_entry))
    process_button.pack(padx=15, pady=10)

    root.mainloop()

# Hauptfunktion
def main():
    """Startet die GUI."""
    gui_erstellen()

if __name__ == "__main__":
    main()


import csv
import os
import tkinter as tk
from tkinter import messagebox

def csv_daten_verarbeiten(data_root):
    """Funktion zur Verarbeitung der CSV-Daten."""
    filenames = os.listdir(data_root)
    all_data = []

    # Durchlaufe alle Dateien im angegebenen Verzeichnis
    for file in filenames:
        uebergabe = os.path.join(data_root, file)  # Erstelle den Pfad

        try:
            with open(uebergabe, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=';')
                raw_data = list(csv_reader)

                # Prüfen, ob die Datei genug Zeilen hat
                if len(raw_data) >= 6:
                    data_without_header = raw_data[5]  # 6. Zeile (Index 5)
                    all_data.append(data_without_header)  # Zeile zur Liste hinzufügen
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Öffnen der Datei {file}: {e}")
            continue  # Überspringe diese Datei und fahre mit der nächsten fort

    return all_data

def daten_speichern(data, output_path):
    """Funktion zum Speichern der verarbeiteten Daten in eine Datei."""
    if os.path.isfile(output_path):
        messagebox.showwarning("Achtung", f"Die Datei {output_path} existiert bereits. Wählen Sie einen anderen Pfad oder löschen Sie die Datei.")
    else:
        try:
            with open(output_path, 'w', newline='') as output_csvfile:
                writer = csv.writer(output_csvfile)
                writer.writerows(data)  # Schreibe die gesammelten Zeilen in die neue Datei
            messagebox.showinfo("Erfolg", f"Die Datei wurde erfolgreich gespeichert unter: {output_path}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Datei: {e}")

def button_klick(path_entry):
    """Funktion, die ausgeführt wird, wenn der Button geklickt wird."""
    data_root = path_entry.get()  # Hol dir den Pfad aus dem Eingabefeld

    # Überprüfen, ob der Pfad existiert
    if not os.path.isdir(data_root):
        messagebox.showerror("Fehler", "Der angegebene Pfad existiert nicht!")
        return

    # Verarbeite die Daten
    all_data = csv_daten_verarbeiten(data_root)

    # Bestimme den Pfad für die Ausgabedatei
    output_path = os.path.join(data_root, "output.csv")

    # Speichere die verarbeiteten Daten
    daten_speichern(all_data, output_path)

def gui_erstellen():
    """Funktion zur Erstellung der GUI mit tkinter."""
    # Hauptfenster der GUI
    root = tk.Tk()
    root.title("CSV Verarbeitungs-Tool")

    # Label für das Eingabefeld
    path_label = tk.Label(root, text="Geben Sie den Pfad zu den CSV-Daten an:")
    path_label.pack(padx=10, pady=10)

    # Eingabefeld für den Pfad
    path_entry = tk.Entry(root, width=50)
    path_entry.pack(padx=10, pady=10)

    # Button, um den Prozess zu starten
    process_button = tk.Button(root, text="Verarbeiten", command=lambda: button_klick(path_entry))
    process_button.pack(padx=10, pady=10)

    # Start der GUI
    root.mainloop()

def main():
    """Hauptfunktion zur Ausführung der Anwendung."""
    gui_erstellen()

if __name__ == "__main__":
    main()

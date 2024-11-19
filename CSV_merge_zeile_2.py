#
#
# import os
# import os
# import tkinter as tk
# from tkinter import filedialog, messagebox
# from tkinter.scrolledtext import ScrolledText
# import pandas as pd
# from openpyxl import load_workbook
#
# # Hilfsfunktion zur Ausgabe in das Text-Widget
# def output_to_widget(text_widget, message):
#     text_widget.insert(tk.END, message + "\n")
#     text_widget.see(tk.END)
#     text_widget.update_idletasks()  # Aktualisiert das Textfeld sofort
#
#
# def extrahiere_exakte_zweite_zeilen(input_folder, output_file):
#     """
#     Liest die zweite Zeile aus allen CSV-Dateien im angegebenen Ordner
#     und speichert sie in einer neuen CSV-Datei.
#
#     :param input_folder: Pfad zum Ordner mit den CSV-Dateien
#     :param output_file: Pfad zur Ausgabedatei
#     """
#     ergebnis_daten = []
#
#     # Überprüfen, ob der Eingabeordner existiert
#     if not os.path.isdir(input_folder):
#         print(f"Fehler: Der Ordner '{input_folder}' existiert nicht.")
#         return
#
#     # Alle Dateien im Ordner durchsuchen
#     for filename in os.listdir(input_folder):
#         if filename.endswith('.csv'):  # Nur CSV-Dateien bearbeiten
#             file_path = os.path.join(input_folder, filename)
#             try:
#                 # Öffnen und nur die zweite Zeile lesen
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     lines = file.readlines()  # Zeilen der Datei lesen
#                     if len(lines) >= 2:  # Mindestens zwei Zeilen vorhanden
#                         zweite_zeile = lines[1].strip()  # Zweite Zeile extrahieren (ohne Leerzeichen)
#                         ergebnis_daten.append(zweite_zeile.split(','))  # Spalten durch Komma trennen
#             except Exception as e:
#                 print(f"Fehler beim Verarbeiten der Datei '{filename}': {e}")
#
#     # Ergebnisse in eine neue CSV-Datei schreiben
#     try:
#         with open(output_file, 'w', encoding='utf-8') as result_file:
#             for daten in ergebnis_daten:
#                 result_file.write(','.join(daten) + '\n')  # Daten als CSV schreiben
#         print(f"Ergebnisdatei erfolgreich erstellt: {output_file}")
#     except Exception as e:
#         print(f"Fehler beim Speichern der Ergebnisdatei: {e}")
#
#
# # Eingabe- und Ausgabepfade definieren
# input_folder = r"K:\Team\Böhmer_Michael\csv"  # Ordner mit den CSV-Dateien
# output_file = os.path.join(input_folder, "Ergebnis.csv")  # Ergebnisdatei im selben Ordner
#
# # Funktion ausführen
# extrahiere_exakte_zweite_zeilen(input_folder, output_file)
#
# # GUI-Setup
# def ordner_auswaehlen(entry):
#     folder_selected = filedialog.askdirectory()
#     entry.delete(0, tk.END)
#     entry.insert(0, folder_selected)
#
# def verabeitung_starten(entry, text_widget):
#     folder_path = entry.get()
#     if not os.path.isdir(folder_path):
#         messagebox.showerror("Fehler", "Bitte geb einen gültigen Ordnerpfad an.")
#         return
#     text_widget.delete(1.0, tk.END)  # Löscht die Textausgabe
#     daten_verarbeiten_speichern(entry, text_widget)
#
# def main():
#     # Hauptfenster erstellen
#     root = tk.Tk()
#     root.title("CSV zusammenlesen Zeile 2")
#
#     # Eingabefeld für Ordnerpfad
#     frame = tk.Frame(root)
#     frame.pack(padx=10, pady=10)
#
#     entry_label = tk.Label(frame, text="Bitte den Ordnerpfad angeben:")
#     entry_label.grid(row=0, column=0, sticky="w")
#
#     # Einstellen der Breite des Eingabefeldes
#     entry = tk.Entry(frame, width=70)
#     entry.grid(row=0, column=1)
#
#     browse_button = tk.Button(frame, text="Durchsuchen", command=lambda: ordner_auswaehlen(entry))
#     browse_button.grid(row=0, column=2, padx=5)
#
#     # Frame für Eingabefelder
#     frame = tk.Frame(root)
#     frame.pack(padx=10, pady=10)
#
#     entry_label1 = tk.Label(frame, text="Pfad für CSV-Dateien:")
#     entry_label1.grid(row=0, column=0, sticky="w")
#
#     # Eingabefeld für Pfad Vorlage
#     entry_blatt1 = tk.Entry(frame, width=70)
#     entry_blatt1.grid(row=0, column=1)
#
#     browse_button1 = tk.Button(frame, text="Durchsuchen", command=lambda: datei_auswaehlen(entry_blatt1))
#     browse_button1.grid(row=0, column=2, padx=5)
#
#     entry_label2 = tk.Label(frame, text="Pfad für Vorlage:")
#     entry_label2.grid(row=1, column=0, sticky="w")
#
#     # Start-Button
#     start_button = tk.Button(frame, text="Starten", command=lambda: verabeitung_starten(entry, text_output))
#     start_button.grid(row=1, column=1, pady=10)
#
#     # Text-Widget für die Ausgaben
#     text_output = ScrolledText(root, height=20, width=100)
#     text_output.pack(padx=10, pady=10)
#
#     root.mainloop()
#
# # Hauptprogramm starten
# if __name__ == "__main__":
#     main()

import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText


def output_to_widget(text_widget, message):
    """Schreibt eine Nachricht in das Textfeld."""
    text_widget.insert(tk.END, message + "\n")
    text_widget.see(tk.END)
    text_widget.update_idletasks()


def extrahiere_zweite_zeilen(input_folder, vorlage_file, output_file, text_widget):
    """
    Liest die zweite Zeile der Vorlagendatei und aller CSV-Dateien im angegebenen Ordner
    und speichert sie in einer neuen CSV-Datei.

    :param input_folder: Pfad zum Ordner mit den CSV-Dateien
    :param vorlage_file: Pfad zur Vorlagendatei
    :param output_file: Pfad zur Ergebnisdatei
    :param text_widget: Widget zur Ausgabe von Informationen
    """
    ergebnis_daten = []

    # Überprüfen, ob die Vorlagendatei existiert
    if not os.path.isfile(vorlage_file):
        messagebox.showerror("Fehler", f"Die Vorlagendatei '{vorlage_file}' existiert nicht.")
        return

    # Zweite Zeile aus der Vorlagendatei extrahieren
    try:
        with open(vorlage_file, 'r') as vorlage:
            lines = vorlage.readlines()
            if len(lines) >= 2:
                vorlage_zeile = lines[1]  # Zweite Zeile extrahieren (unverändert)
                ergebnis_daten.append(vorlage_zeile)
                output_to_widget(text_widget, f"Vorlage verarbeitet: {vorlage_file}")
            else:
                output_to_widget(text_widget, f"Vorlage hat keine zweite Zeile: {vorlage_file}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Verarbeiten der Vorlage: {e}")
        return

    # Durchsuche den Eingabeordner nach CSV-Dateien
    if not os.path.isdir(input_folder):
        messagebox.showerror("Fehler", f"Der Ordner '{input_folder}' existiert nicht.")
        return

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):  # Nur CSV-Dateien bearbeiten
            file_path = os.path.join(input_folder, filename)
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    if len(lines) >= 2:
                        zweite_zeile = lines[1]  # Zweite Zeile extrahieren (unverändert)
                        ergebnis_daten.append(zweite_zeile)
                        output_to_widget(text_widget, f"Datei verarbeitet: {filename}")
                    else:
                        output_to_widget(text_widget, f"Datei hat keine zweite Zeile: {filename}")
            except Exception as e:
                output_to_widget(text_widget, f"Fehler beim Verarbeiten der Datei '{filename}': {e}")

    # Ergebnisse in eine neue CSV-Datei schreiben
    try:
        with open(output_file, 'w') as result_file:
            for daten in ergebnis_daten:
                result_file.write(daten)  # Zeile unverändert in die Datei schreiben
        output_to_widget(text_widget, f"Ergebnisdatei erstellt: {output_file}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Speichern der Ergebnisdatei: {e}")


def ordner_auswaehlen(entry):
    """Öffnet einen Dialog zur Ordnerauswahl."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry.delete(0, tk.END)
        entry.insert(0, folder_selected)


def datei_auswaehlen(entry):
    """Öffnet einen Dialog zur Dateiauswahl."""
    file_selected = filedialog.askopenfilename(filetypes=[("CSV-Dateien", "*.csv")])
    if file_selected:
        entry.delete(0, tk.END)
        entry.insert(0, file_selected)


def starte_verarbeitung(entry_folder, entry_vorlage, text_widget):
    """Startet die Verarbeitung der Dateien."""
    input_folder = entry_folder.get()
    vorlage_file = entry_vorlage.get()
    output_file = os.path.join(input_folder, "Ergebnis.csv")

    if not input_folder or not vorlage_file:
        messagebox.showerror("Fehler", "Bitte sowohl den Ordner als auch die Vorlagendatei angeben.")
        return

    extrahiere_zweite_zeilen(input_folder, vorlage_file, output_file, text_widget)


def gui_erstellen():
    """Erstellt die GUI."""
    root = tk.Tk()
    root.title("CSV-Verarbeitung: Zweite Zeile extrahieren")

    # Ordnerauswahl
    folder_frame = tk.Frame(root)
    folder_frame.pack(pady=5, padx=10, fill=tk.X)
    folder_label = tk.Label(folder_frame, text="CSV-Ordner auswählen:")
    folder_label.pack(side=tk.LEFT, padx=5)
    folder_entry = tk.Entry(folder_frame, width=60)
    folder_entry.pack(side=tk.LEFT, padx=5)
    folder_button = tk.Button(folder_frame, text="Durchsuchen", command=lambda: ordner_auswaehlen(folder_entry))
    folder_button.pack(side=tk.LEFT, padx=5)

    # Vorlagendatei-Auswahl
    vorlage_frame = tk.Frame(root)
    vorlage_frame.pack(pady=5, padx=10, fill=tk.X)
    vorlage_label = tk.Label(vorlage_frame, text="Vorlagendatei auswählen:")
    vorlage_label.pack(side=tk.LEFT, padx=5)
    vorlage_entry = tk.Entry(vorlage_frame, width=60)
    vorlage_entry.pack(side=tk.LEFT, padx=5)
    vorlage_button = tk.Button(vorlage_frame, text="Durchsuchen", command=lambda: datei_auswaehlen(vorlage_entry))
    vorlage_button.pack(side=tk.LEFT, padx=5)

    # Start-Button
    start_button = tk.Button(root, text="Starten", command=lambda: starte_verarbeitung(folder_entry, vorlage_entry, text_output))
    start_button.pack(pady=10)

    # Textfeld für Ausgabe
    text_output = ScrolledText(root, height=20, width=80)
    text_output.pack(pady=5, padx=10)

    root.mainloop()


if __name__ == "__main__":
    gui_erstellen()


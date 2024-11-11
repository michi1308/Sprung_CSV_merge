import pandas as pd


def csv_datei_lesen_und_werte_splitten(file_path):
    """Liest die CSV-Datei und splitte die Werte in der ersten Zelle jeder Zeile."""
    try:
        # Verwende den Kontextmanager (with), um sicherzustellen, dass die Datei korrekt geschlossen wird
        df = pd.read_csv(file_path, header=None, encoding='utf-8')
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return None
    # Splitte die Daten in der ersten Spalte, die durch Tabulatoren getrennt sind
    data = df[0].str.split('\t', expand=True)
    return data


# def konvertiere_zahlen_von_punkt_zu_komma(data):
#     """Konvertiere Dezimalzahlen von Punkt zu Komma und behalte den numerischen Typ."""
#     if data is None:
#         return None
#
#     def punkt_zu_komma(value):
#         """Hilfsfunktion, um Punkt durch Komma zu ersetzen und dann als Zahl zu behandeln."""
#         # Zuerst den Punkt durch ein Komma ersetzen
#         value_str = str(value).replace('.', ',')
#
#         # Versuche, den Wert als float zu behandeln:
#         try:
#             # Den Wert als float behandeln (Komma durch Punkt ersetzen)
#             return float(value_str.replace(',', '.'))
#         except ValueError:
#             # Falls die Konvertierung nicht möglich ist, gebe den Wert als Text zurück
#             return value_str
#
#     # Wende die Hilfsfunktion auf jedes Element des DataFrames an
#     return data.applymap(punkt_zu_komma)


def konvertiere_zahlen_von_punkt_zu_komma(data):
    """Konvertiere Dezimalzahlen von Punkt zu Komma und behalte den numerischen Typ."""
    if data is None:
        return None

    def punkt_zu_komma(value):
        """Hilfsfunktion, um Punkt durch Komma zu ersetzen und dann als Zahl zu behandeln."""
        value_str = str(value).replace('.', ',')
        try:
            return float(value_str.replace(',', '.'))
        except ValueError:
            return value_str

    # Iteriere durch alle Spalten und wende 'map' an
    for spalte in data.columns:
        data[spalte] = data[spalte].map(punkt_zu_komma)

    return data


# def konvertiere_zahlen_von_punkt_zu_komma(data):
#     """Konvertiere Dezimalzahlen von Punkt zu Komma."""
#     if data is None:
#         return None
#     return data.apply(lambda x: x.astype(str).replace('.', ','))
#

def daten_speichern(data, output_path):
    """Speichert die Daten in einer Excel-Datei."""
    if data is None:
        print("Keine Daten zum Speichern.")
        return
    try:
        # Verwende den Kontextmanager (with), um sicherzustellen, dass die Excel-Datei korrekt geschlossen wird
        data.to_excel(output_path, index=False, header=False)
        print(f'Datei erfolgreich gespeichert als {output_path}')
    except Exception as e:
        print(f"Fehler beim Speichern der Excel-Datei: {e}")


def main():
    input_file = r"K:\Team\Böhmer_Michael\test\output.csv"
    output_file = r"K:\Team\Böhmer_Michael\test\output_converted.xlsx"

    # Schritt 1: Einlesen und Splitten der CSV-Daten
    data = csv_datei_lesen_und_werte_splitten(input_file)

    # Schritt 2: Dezimalstellen anpassen (Punkt in Komma umwandeln)
    data_with_comma = konvertiere_zahlen_von_punkt_zu_komma(data)

    # Schritt 3: Speichern der bearbeiteten Daten als Excel
    daten_speichern(data_with_comma, output_file)


if __name__ == '__main__':
    main()

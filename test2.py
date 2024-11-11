import pandas as pd


def csv_datei_lesen_und_werte_splitten(file_path):
    """Liest die CSV-Datei und splitte die Werte in der ersten Zelle jeder Zeile."""
    try:
        df = pd.read_csv(file_path, header=None, encoding='utf-8')
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return None
    data = df[0].str.split('\t', expand=True)
    return data


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


def daten_speichern(data, output_path):
    """Speichert die Daten in einer Excel-Datei."""
    if data is None:
        print("Keine Daten zum Speichern.")
        return
    try:
        data.to_excel(output_path, index=False, header=False)
        print(f'Datei erfolgreich gespeichert als {output_path}')
    except Exception as e:
        print(f"Fehler beim Speichern der Excel-Datei: {e}")


def hole_vorlage(file_path, num_rows=5):
    """Liest die ersten 'num_rows' Zeilen einer Excel-Vorlage."""
    try:
        # Lese die Excel-Datei und nimm nur die ersten 'num_rows' Zeilen
        template_df = pd.read_excel(file_path, header=None)
        return template_df.head(num_rows)  # Holen der ersten 'num_rows' Zeilen
    except Exception as e:
        print(f"Fehler beim Lesen der Vorlage: {e}")
        return None


def main():
    input_file = r"K:\Team\Böhmer_Michael\test\output.csv"
    output_file = r"K:\Team\Böhmer_Michael\test\output_converted.xlsx"
    template_file = r"K:\Team\Böhmer_Michael\Vorlagen\CSV_merge_Sprünge_Vorlage_Header.xlsx"

    # Schritt 1: Einlesen und Splitten der CSV-Daten
    data = csv_datei_lesen_und_werte_splitten(input_file)

    # Schritt 2: Dezimalstellen anpassen (Punkt in Komma umwandeln)
    data_with_comma = konvertiere_zahlen_von_punkt_zu_komma(data)

    # Schritt 3: Hole die ersten 5 Zeilen der Vorlage
    template_data = hole_vorlage(template_file)

    # Schritt 4: Füge die Vorlage oben zu den bearbeiteten Daten hinzu
    if template_data is not None:
        # Füge die Daten zusammen (Vorlage oben, dann die verarbeiteten Daten)
        combined_data = pd.concat([template_data, data_with_comma], ignore_index=True)
    else:
        combined_data = data_with_comma

    # Schritt 5: Speichern der bearbeiteten Daten als Excel
    daten_speichern(combined_data, output_file)


if __name__ == '__main__':
    main()


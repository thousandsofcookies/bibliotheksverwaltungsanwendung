import database as db  # Importiert das benutzerdefinierte Modul 'database', das für die Datenbankoperationen zuständig ist
import gui  # Importiert das benutzerdefinierte Modul 'gui', das die grafische Benutzeroberfläche (GUI) steuert

# Überprüft, ob das Skript direkt ausgeführt wird (nicht als importiertes Modul)
if __name__ == "__main__":
    db.create_table()  # Erstellt die Datenbank und die notwendige Tabelle(n), falls diese noch nicht existieren
    gui.run_app()      # Startet die grafische Benutzeroberfläche (GUI) der Anwendung
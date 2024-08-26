import database as db
import gui

if __name__ == "__main__":
    db.create_table()  # Datenbank und Tabelle erstellen
    gui.run_app()      # GUI starten
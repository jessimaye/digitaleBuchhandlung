# Masterarbeit: Benutzerzentrierte Entwicklung einer digitalen Buchhandlung

## Prototyp starten

Um die Virtuelle Environment anzulegen und zu starten:
```
python -m venv .venv
source .venv/bin/activate  # oder Windows:  .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Im backend-Ordner eine .env-Datei mit dem Huggingface-Token anlegen (HG_TOKEN):
```
HG_TOKEN="<hier_den_token_einfuegen>"
```
Den Token bei Huggingface unter "Settings" und "Access Tokens" erstellen und bei "Permissions" Write ausfwählen. 

In den Ordner backend das Korpus mit den Fanfiction-Texten einfügen.

Prototyp immer über app.py starten und über http://127.0.0.1:5000/home die Startseite öffnen.

## Aufbau 

Der Ordner Prototyp enthält alle Code-Dateien für den Prototyp, hinzugefügt werden müssen nur noch das Korpus
sowie die .env-Datei mit dem Huggingface-Token. Im Ordner backend befinden sich die Flask-App sowie die Dateien für die RAG-Pipeline samt Preprocessing. Im Ordner frontend befinden sich die HTML-Seiten, die CSS-Datei für das Sytling, der JavaScript-Code sowie die für den Prototyp verwendeten Bilder. 

Der Ordner Umfrage_Auswertung enthält das JupyterNotebook, das zur Analyse der Umfrage-Ergebnisse verwendet wurde sowie die dazu erstellten Plots. 

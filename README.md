# Masterarbeit: Benutzerzentrierte Entwicklung einer digitalen Buchhandlung – Prototyp

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
Den Token bei Huggingface unter "Settings" und "Access Tokens" erstellen und bei "Permissions" Write auswählen. 

In den Ordner backend das Korpus mit den Fanfiction-Texten einfügen.

Prototyp immer über app.py starten und über http://127.0.0.1:5000/home die Startseite öffnen.

## Aufbau 

Dieses Repository enthält alle Code-Dateien für den Prototyp, hinzugefügt werden müssen nur noch das Korpus
sowie die .env-Datei mit dem Huggingface-Token. Im Ordner backend befinden sich die Flask-App sowie die Dateien für die RAG-Pipeline samt Preprocessing. Im Ordner frontend liegen die HTML-Seiten, die CSS-Datei für das Styling, der JavaScript-Code sowie die für den Prototyp verwendeten Bilder. 


from flask import Flask, render_template, request, jsonify
from rag_pipeline import rag_pipeline, document_store
from preprocessing import run_preprocessing_pipeline
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
import os
from pathlib import Path 



base_dir = Path(__file__).parent.parent
frontend_dir = base_dir/"frontend"

app = Flask(__name__, template_folder=str(frontend_dir), static_folder=str(frontend_dir), static_url_path="")

#beim Starten des Prototyps die Texte samt Metadaten aus den json-Dateien in den Document Store laden
def index_documents_if_empty ():
    if document_store.count_documents() == 0:

        output_dir = Path("backend/Korpus")  # Pfad zum Verzeichnis, wo sich die json-Dateien befinden
        run_preprocessing_pipeline(output_dir)


with app.app_context():
    index_documents_if_empty()


#html-Seiten über die Flask-App starten, damit sie über localhost aufrufbar sind
@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/detail")
def detail():
    return render_template("detail.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/home")
def home_page():
    return render_template("index.html")

@app.route("/recommendation")
def recommendation_page():
    return render_template("recomm.html")

#Schnittstelle zur Rag-Pipeline
#Frage(User-Input) wird über JavaScript abgerufen und an Flask-Schnittstelle gesendet
#und damit die Rag-Pipeline aktiviert, um die Frage zu beantworten
@app.route("/chat", methods=["POST"])
def chat():
        data = request.json #Umwandeln in JavaScript-Objekt
        question = data.get("question", "").strip()
        history = data.get("history",[])

        if not question:
            return jsonify ({"error":"Keine Frage erhalten"}), 400
        
        try:
            result = rag_pipeline.run({
                "text_embedder":{"text":question},
                "prompt_builder":{"question":question}
            })

            answer = result["llm"]["replies"][0].text

            #Neue Nachrichten zum Kontext (History) hinzufügen
            new_history = history + [
                {"role":"user", "content":question},
                {"role":"assistant","content":answer}
            ]

            return jsonify({
                "answer":answer,
                "history":new_history,
            })
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
if __name__ == "__main__":
    app.run(debug=True, port=5000)
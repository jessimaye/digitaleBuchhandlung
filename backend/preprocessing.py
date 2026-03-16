from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.writers import DocumentWriter
from haystack.components.converters import TextFileToDocument, JSONConverter
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.utils import Secret
from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.components.builders.chat_prompt_builder import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from pathlib import Path
import json 

from rag_pipeline import document_store

#Preprocessing-Pipeline bauen
#kann json-Dateien mit Metadaten einlesen, unter dem key "text" ist die Geschichte gespeichert


document_cleaner = DocumentCleaner()
document_splitter = DocumentSplitter(split_by="word", split_length=150, split_overlap=50)

preprocessing_pipeline = Pipeline()
preprocessing_pipeline.add_component(instance=document_cleaner, name="document_cleaner")
preprocessing_pipeline.add_component(instance=document_splitter, name="document_splitter")

#Metadaten (Titel, Autor, Fandom und Charaktere) zur Pipeline hinzufügen
document_embedder = SentenceTransformersDocumentEmbedder(
    model="intfloat/multilingual-e5-small",
    meta_fields_to_embed=["title","author","fandom","character"],
    embedding_separator="\n")
document_embedder.warm_up()
preprocessing_pipeline.add_component(instance=document_embedder, name="document_embedder")

document_writer = DocumentWriter(document_store=document_store)
preprocessing_pipeline.add_component(instance=document_writer, name="document_writer")

preprocessing_pipeline.connect("document_cleaner", "document_splitter")
preprocessing_pipeline.connect("document_splitter", "document_embedder")
preprocessing_pipeline.connect("document_embedder", "document_writer")

def run_preprocessing_pipeline(folder_path):
    folder_path = Path(folder_path)
    json_files = list(folder_path.glob("*.json"))

    #json-Dateien mit Metafeldern laden und daraus Documents erstellen
    json_docs = []
    for file in json_files: 
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            doc = Document(
                content = data.get("text",""),
                meta = {
                    "title":data.get("title",""),
                    "author":data.get("author",""),
                    "fandom":data.get("fandom",""),
                    "character":data.get("character",""),
                })
            json_docs.append(doc)
    
    #json-Documents ab Cleaner in Pipeline einspielen 
    if json_docs:
        preprocessing_pipeline.run({"document_cleaner": {"documents": json_docs}})


from haystack import Pipeline
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
from dotenv import load_dotenv
import os

load_dotenv()

#RAG-Pipeline bauen 
document_store = InMemoryDocumentStore()

template = [
    ChatMessage.from_system(
        """Du bist ein hilfreicher Chatbot, der Gustave heißt und Empfehlungen für Geschichten gibt. 
        
        Wenn der User ein Buch, einen Autor, ein Genre, ein Thema oder ähnliches nennt, das ihm gefallen hat, empfiehlst du anhand des folgenden Kontexts passende Geschichten. 
        
        Der verfügbare Kontext enthält Geschichten sowie folgende Metadaten:
            - Titel
            - Autor
            - Fandom
            - Charaktere

        Verwende diese Informationen, um präzise und passende Empfehlungen zu geben. Die Empfehlung muss eine kurze Inhaltsangabe und Einordnung der Geschichte enthalten. Wenn der User einen Autor nennt, von dem er gerne Bücher liest, nenne ihn Geschichten aus dem Kontext, die ähnlich wie diese Bücher sind. Wenn der User ein Buch nennt, das ihm gefallen hat, empfehle ihm Geschichten aus dem Kontext, die ähnlich wie dieses Buch sind, beispielsweise ähnliche Themen, einen ähnlichen Schreibstil oder ein ähnliches Genre hat. 

        Aktueller Kontext:
        {% for doc in documents %}
        Titel: {{ doc.meta.title | default("unbekannt") }}
        Autor: {{ doc.meta.author | default("unbekannt") }}
        Fandom: {{ doc.meta.fandom | default("kein Fandom") }}
        Charaktere: {{ doc.meta.character | default("keine Angabe") }}

        Inhalt:
        {{ doc.content }}

        {% endfor %}

        Antworte ausschließlich basierend auf diesem Kontext. 
        Wenn die Information nicht im Kontext steht, sage, dass es in dieser Buchhandlung keine passende Empfehlung gibt. Wenn Du eine Frage des Users nicht verstehst oder etwas unklar ist, frage bitte nach."""
    ),
    ChatMessage.from_user("{{ question }}")
]


def build_rag_pipeline ():
    text_embedder = SentenceTransformersTextEmbedder(model="intfloat/multilingual-e5-small")
    text_embedder.warm_up()

    retriever = InMemoryEmbeddingRetriever(document_store=document_store)

    prompt_builder = ChatPromptBuilder(template=template, required_variables=["documents","question"])

    #token bei Hugging-Face unter Access-Token erstellen, wichtig: write!
    generator = HuggingFaceAPIChatGenerator(api_type="serverless_inference_api",
                                    api_params={"model": "meta-llama/Llama-3.3-70B-Instruct"},
                                    token=Secret.from_token(os.getenv("HG_TOKEN")))
    
    rag_pipeline = Pipeline()
    rag_pipeline.add_component("text_embedder", text_embedder)
    rag_pipeline.add_component("retriever", retriever)
    rag_pipeline.add_component("prompt_builder", prompt_builder)
    rag_pipeline.add_component("llm", generator)

    rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    rag_pipeline.connect("retriever.documents", "prompt_builder.documents")
    rag_pipeline.connect("prompt_builder.prompt", "llm.messages")

    return rag_pipeline 

rag_pipeline = build_rag_pipeline()


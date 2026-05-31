import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
# Cambiamos la importación de Google por la de HuggingFace
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.ports.vector_store_port import VectorStorePort

load_dotenv()

class FaissAdapter(VectorStorePort):
    def __init__(self):
        print("📦 Cargando modelo de embeddings local de HuggingFace (all-MiniLM-L6-v2)...")
        # Este modelo se descargará automáticamente la primera vez (90MB) 
        # y las siguientes veces arrancará al instante.
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db = None
        print("✅ Modelo local cargado y listo. ¡Adiós dependencias de Google!")

    def guardar_texto(self, texto: str) -> None:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        fragmentos = text_splitter.split_text(texto)
        
        if fragmentos:
            print(f"🧠 Procesando localmente {len(fragmentos)} fragmentos en FAISS...")
            self.db = FAISS.from_texts(fragmentos, self.embeddings)
            print("✅ Base de datos FAISS guardada en memoria local.")

    def buscar_similares(self, consulta: str, k: int = 3) -> str:
        if not self.db:
            print("⚠️ Base de datos vacía. Sube un PDF primero.")
            return "" 
        
        documentos_relevantes = self.db.similarity_search(consulta, k=k)
        contexto_encontrado = "\n\n".join([doc.page_content for doc in documentos_relevantes])
        return contexto_encontrado
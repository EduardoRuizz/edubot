import os
import json
import uuid
import sqlite3
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ==========================================
# IMPORTACIONES DE TU ARQUITECTURA (Hexagonal)
# ==========================================
from app.adapters.ai.gemini_adapter import GeminiAdapter 
from app.adapters.db.faiss_adapter import FaissAdapter
from app.core.services.agent_service import AgentService

# IMPORTACIÓN IMPORTANTE: Traemos la inicialización desde su nueva carpeta
from app.adapters.db.database import init_db

# ==========================================
# 1. INICIALIZACIÓN DE LA APP Y BASE DE DATOS
# ==========================================
app = FastAPI(title="EduBot AI Pro Backend")

# Habilitar CORS por si tu frontend corre en otro puerto local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "edubot_historial.db"

# Llamamos a la función importada para asegurar que las tablas existan al arrancar
init_db()

# ==========================================
# 2. INYECCIÓN DE DEPENDENCIAS (Componentes)
# ==========================================
vector_db = FaissAdapter()
ai_adapter = GeminiAdapter()
agente = AgentService(ai_adapter=ai_adapter, vector_db=vector_db)

# ==========================================
# 3. RUTAS DE LA INTERFAZ WEB
# ==========================================
@app.get("/", response_class=HTMLResponse)
def obtener_interfaz():
    """Sirve la página web principal de la aplicación."""
    ruta_index = os.path.join("templates", "index.html")
    if not os.path.exists(ruta_index):
        return """
        <div style="font-family:sans-serif; text-align:center; padding:50px;">
            <h2>⚠️ Archivo index.html no encontrado</h2>
            <p>Asegúrate de tener tu HTML guardado en la carpeta <strong>templates/index.html</strong></p>
        </div>
        """
    with open(ruta_index, "r", encoding="utf-8") as archivo:
        return archivo.read()

# ==========================================
# 4. RUTAS DEL HISTORIAL DE CHATS (Manejo de Persistencia)
# ==========================================
@app.get("/historial")
def obtener_historial():
    """Devuelve la lista de todas las sesiones de chat guardadas para la barra lateral."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo FROM chats ORDER BY fecha DESC")
        chats = [{"id": r[0], "titulo": r[1]} for r in cursor.fetchall()]
        conn.close()
        return chats
    except Exception as e:
        print(f"Error al obtener historial: {e}")
        return []

@app.get("/historial/{chat_id}")
def obtener_mensajes_chat(chat_id: str):
    """Devuelve los mensajes pasados de un chat específico al seleccionarlo."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT remitente, tipo, contenido FROM mensajes WHERE chat_id = ? ORDER BY id ASC", (chat_id,))
        filas = cursor.fetchall()
        conn.close()
        
        mensajes = []
        for r in filas:
            remitente, tipo, contenido_raw = r[0], r[1], r[2]
            try:
                contenido = json.loads(contenido_raw)
            except:
                contenido = contenido_raw
                
            mensajes.append({
                "remitente": remitente,
                "tipo": tipo,
                "contenido": contenido
            })
        return mensajes
    except Exception as e:
        print(f"Error al cargar mensajes del chat {chat_id}: {e}")
        return []

# ==========================================
# 5. RUTAS DEL NÚCLEO CORE (Chat y Carga de PDF)
# ==========================================
@app.get("/chat")
def chat_endpoint(pregunta: str, chat_id: str = Query(...)):
    """Procesa el mensaje del usuario, guarda en historial y responde usando el Agente."""
    if not pregunta.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Registrar chat nuevo si no existe
        cursor.execute("SELECT id FROM chats WHERE id = ?", (chat_id,))
        if not cursor.fetchone():
            titulo_conversacion = pregunta[:28] + "..." if len(pregunta) > 28 else pregunta
            cursor.execute("INSERT INTO chats (id, titulo) VALUES (?, ?)", (chat_id, titulo_conversacion))
        
        # 2. Registrar el mensaje del usuario
        cursor.execute("INSERT INTO mensajes (chat_id, remitente, tipo, contenido) VALUES (?, ?, ?, ?)", 
                       (chat_id, "usuario", "texto", json.dumps(pregunta)))
        
        # 3. Invocar al Agente Inteligente (Groq / Llama)
        respuesta_agente = agente.procesar_interaccion(mensaje_usuario=pregunta)
        
        # 4. Registrar la respuesta generada
        cursor.execute("INSERT INTO mensajes (chat_id, remitente, tipo, contenido) VALUES (?, ?, ?, ?)", 
                       (chat_id, "bot", respuesta_agente["tipo"], json.dumps(respuesta_agente["contenido"])))
        
        conn.commit()
        conn.close()
        
        return respuesta_agente

    except Exception as error:
        print(f"❌ Error en chat_endpoint: {error}")
        return {
            "tipo": "texto",
            "contenido": "Lo siento, tuve un problema interno al guardar o procesar tu mensaje. ¡Inténtalo de nuevo!"
        }

@app.post("/subir-pdf")
async def subir_pdf(archivo: UploadFile = File(...)):
    """Endpoint para procesar el archivo PDF del estudiante y guardarlo en el FAISS local."""
    try:
        if not archivo.filename.endswith('.pdf'):
            return {"status": "error", "message": "El archivo proporcionado debe ser un PDF válido."}
            
        from pypdf import PdfReader
        
        contenido_bytes = await archivo.read()
        
        with open("temporal.pdf", "wb") as f:
            f.write(contenido_bytes)
            
        lector = PdfReader("temporal.pdf")
        texto_completo = ""
        for pagina in lector.pages:
            texto_completo += pagina.extract_text() + "\n"
            
        if os.path.exists("temporal.pdf"):
            os.remove("temporal.pdf")
            
        if not texto_completo.strip():
            return {"status": "error", "message": "No pudimos extraer texto del archivo (¿Es un PDF escaneado como imagen?)"}
            
        vector_db.guardar_texto(texto_completo)
        
        return {"status": "exito", "message": "PDF analizado e indexado de manera local con HuggingFace."}
        
    except Exception as e:
        print(f"Error procesando el PDF: {e}")
        return {"status": "error", "message": f"Ocurrió un error inesperado: {str(e)}"}
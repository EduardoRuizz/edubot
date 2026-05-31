# EduBot AI Pro - Sistema de Tutoría Inteligente (RAG)

Este sistema implementa un entorno de tutoría automatizada y evaluación dinámica aplicando **Arquitectura Hexagonal (Puertos y Adaptadores)**. Permite la ingesta de documentos PDF, indexación semántica local y generación de respuestas/quizzes interactivos en tiempo real.

---

## 🛠️ Stack Tecnológico y Requerimientos

El proyecto está diseñado de forma modular utilizando los siguientes componentes de infraestructura:

1. **Servidor de Aplicaciones:** FastAPI & Uvicorn (Inferencia asíncrona).
2. **Motor de Búsqueda Semántica:** FAISS (Facebook AI Similarity Search) en memoria.
3. **Modelos de Embeddings (Local):** HuggingFace (`all-MiniLM-L6-v2`) operando al 100% en hardware local para eliminar latencia de red.
4. **Cerebro Cognitivo (Nube):** Groq Cloud ejecutando el LLM `Llama-3.3-70b-versatile` para procesamiento de lenguaje natural y estructuración estricta de JSON.
5. **Persistencia Relacional:** SQLite para el almacenamiento local del historial de conversaciones.

---

## 🏗️ Estructura del Proyecto (Arquitectura Hexagonal)

La distribución de directorios refleja el aislamiento de la lógica de negocio frente a las herramientas tecnológicas:

```text
edubot/
├── app/
│   ├── adapters/            # Capa de Infraestructura (Contacto con el exterior)
│   │   ├── ai/
│   │   │   └── gemini_adapter.py  # Implementación de inferencia con Groq
│   │   └── db/
│   │       ├── database.py       # Persistencia relacional de chats (SQLite)
│   │       └── faiss_adapter.py  # Persistencia vectorial (HuggingFace Embeddings)
│   ├── core/                # Capa Central (Reglas de Negocio Puras)
│   │   ├── ports/
│   │   │   ├── ai_port.py        # Contrato de interfaces para la IA
│   │   │   └── vector_store_port.py
│   │   └── services/
│   │       └── agent_service.py  # Orquestador cognitivo e intención del usuario
│   └── main.py              # Punto de entrada de la API y cableado de dependencias
├── templates/
│   └── index.html           # Interfaz de Usuario (Dashboard estilo SaaS)
├── requirements.txt         # Manifiesto de requerimientos y dependencias
└── .env                     # Variables de entorno confidenciales (Claves de API)

🚀 Instrucciones de Despliegue Técnico
Siga este protocolo secuencial para inicializar el sistema en un entorno aislado:

1. Inicialización del Entorno de Ejecución
Genere un entorno virtual de Python para mitigar conflictos con dependencias globales de la máquina hospedadora:

Bash
python -m venv venv
Active el entorno virtual según su sistema operativo:

Windows (PowerShell/CMD):

Bash
.\venv\Scripts\activate
Unix / macOS:

Bash
source venv/bin/activate

2. Instalación del Manifiesto de Requerimientos
Asegure el aprovisionamiento de todos los paquetes y librerías del ecosistema ejecutando:

Bash
pip install -r requirements.txt

3. Configuración del Entorno de Red (.env)

El proyecto ya incluye un archivo `.env` configurado con una API Key activa de Groq Cloud dentro de este repositorio privado para facilitar su evaluación inmediata. No requiere configuración adicional.

4. Lanzamiento del Servidor de Aplicaciones
Despliegue el backend asíncrono con escucha activa y recarga en caliente para desarrollo:

Bash
uvicorn app.main:app --reload
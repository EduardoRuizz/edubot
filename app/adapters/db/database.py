import sqlite3
import json

DB_PATH = "edubot_historial.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Tabla para los hilos de conversación (Temas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id TEXT PRIMARY KEY,
            titulo TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Tabla para los mensajes de cada chat
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            remitente TEXT,
            tipo TEXT,
            contenido TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_id) REFERENCES chats(id)
        )
    """)
    conn.commit()
    conn.close()

# Inicializamos la base de datos de inmediato al importar
init_db()
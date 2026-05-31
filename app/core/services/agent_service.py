import json
import re
from app.core.ports.ai_port import AIPort
from app.core.ports.vector_store_port import VectorStorePort

class AgentService:
    def __init__(self, ai_adapter: AIPort, vector_db: VectorStorePort):
        self.ai = ai_adapter
        self.db = vector_db

    def procesar_interaccion(self, mensaje_usuario: str) -> dict:
        """
        Agente unificado con detección dinámica de cantidad de preguntas para el examen.
        """
        try:
            contexto = self.db.buscar_similares(mensaje_usuario, k=3)
            
            # Buscamos si el usuario escribió algún número en su mensaje (ej. "6 preguntas", "un test de 5")
            numeros_encontrados = re.findall(r'\b\d+\b', mensaje_usuario)
            
            # Si encontró un número, usamos ese; si no, dejamos 5 como el estándar profesional
            num_preguntas = int(numeros_encontrados[0]) if numeros_encontrados else 5
            
            # Limitamos por seguridad para que no le pidan un examen de 100 preguntas y rompa Groq
            if num_preguntas > 15:
                num_preguntas = 15

            # Unificamos la clasificación y la generación en un solo prompt inyectando la variable
            prompt_unico = f"""
            Actúa como un tutor académico de IA inteligente. Analiza el mensaje del usuario y el contexto del PDF provisto.
            Debes responder ÚNICAMENTE con un objeto JSON válido, sin bloques de código markdown (no uses ```json).
            
            EVALUACIÓN DE INTENCIÓN:
            1. Si el usuario te hace una pregunta normal o te pide explicar algo, responde usando este formato:
            {{
                "tipo": "texto",
                "contenido": "Aquí va tu respuesta explicativa detallada y amigable basada en el contexto."
            }}
            
            2. Si el usuario pide explícitamente un examen, test, quiz o evaluar sus conocimientos, genera un examen de opción múltiple de EXACTAMENTE {num_preguntas} PREGUNTAS basado en el contexto usando este formato estricto:
            {{
                "tipo": "quiz",
                "contenido": {{
                    "preguntas": [
                        {{
                            "id": 1,
                            "pregunta": "Texto de la primera pregunta de examen aquí",
                            "opciones": {{
                                "A": "Opción A",
                                "B": "Opción B",
                                "C": "Opción C",
                                "D": "Opción D"
                            }},
                            "correcta": "Letra de la correcta (A, B, C o D)",
                            "retroalimentacion": "Explicación breve de por qué es la correcta"
                        }}
                    ]
                }}
            }}

            IMPORTANTE: Si generas un quiz, el array de "preguntas" debe tener exactamente {num_preguntas} elementos.
            
            CONTEXTO DEL PDF: {contexto}
            MENSAJE DEL USUARIO: "{mensaje_usuario}"
            RESPUESTA JSON:"""
            
            # Llamada unificada a Groq
            respuesta_raw = self.ai.responder_pregunta(pregunta=prompt_unico)
            
            # Limpieza de seguridad
            respuesta_clean = respuesta_raw.replace("```json", "").replace("```", "").strip()
            
            # Convertimos la respuesta a diccionario
            datos_retorno = json.loads(respuesta_clean)
            return datos_retorno

        except Exception as error:
            print(f"⚠️ Error en llamada unificada: {error}")
            return {
                "tipo": "texto", 
                "contenido": "Tuve un pequeño problema al procesar tu solicitud. ¿Podrías intentar preguntármelo de otra forma?"
            }
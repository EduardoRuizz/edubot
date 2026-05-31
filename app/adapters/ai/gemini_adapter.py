import os
from langchain_groq import ChatGroq
from app.core.ports.ai_port import AIPort

class GeminiAdapter(AIPort): # Mantenemos el nombre de la clase para no romper nada
    def __init__(self):
        # Inicializamos Groq con Llama 3.3, que es súper inteligente y vuela en velocidad
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            api_key=os.getenv("GROQ_API_KEY")
        )

    def responder_pregunta(self, pregunta: str, contexto: str = "") -> str:
        if contexto:
            prompt = f"Contexto extraído del PDF:\n{contexto}\n\nPregunta: {pregunta}"
        else:
            prompt = pregunta
            
        respuesta = self.llm.invoke(prompt)
        return respuesta.content

    def generar_examen(self, texto_base: str) -> str:
        # Este método ya no se usará tanto si usas la llamada unificada, 
        # pero lo dejamos aquí por compatibilidad de tu estructura
        prompt = f"Genera un examen en formato JSON estricto basado en este texto:\n{texto_base}"
        respuesta = self.llm.invoke(prompt)
        return respuesta.content
from abc import ABC, abstractmethod

class AIPort(ABC):
    """
    Esta es la interfaz (Puerto).
    Define qué debe hacer cualquier IA que conectemos a nuestro sistema.
    """
    
    @abstractmethod
    def responder_pregunta(self, pregunta: str, contexto: str = "") -> str:
        pass

    @abstractmethod
    def generar_examen(self, texto_base: str) -> str:
        pass
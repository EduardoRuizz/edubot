from abc import ABC, abstractmethod

class VectorStorePort(ABC):
    @abstractmethod
    def guardar_texto(self, texto: str) -> None:
        """Contrato para dividir texto y guardarlo en la BD Vectorial"""
        pass

    @abstractmethod
    def buscar_similares(self, consulta: str, k: int = 3) -> str:
        """Contrato para recuperar los fragmentos más relevantes basados en una pregunta"""
        pass
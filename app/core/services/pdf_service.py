import io
from pypdf import PdfReader

def extraer_texto_pdf(contenido_bytes: bytes) -> str:
    """
    Recibe el archivo PDF en bytes, procesa sus páginas y devuelve todo el texto extraído.
    """
    try:
        lector = PdfReader(io.BytesIO(contenido_bytes))
        texto = ""
        for pagina in lector.pages:
            texto += pagina.extract_text() or ""
        return texto
    except Exception as e:
        return f"Error al procesar el archivo PDF: {str(e)}"
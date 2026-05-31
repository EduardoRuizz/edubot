from langchain_text_splitters import RecursiveCharacterTextSplitter

def test_particion_texto_respeta_limites():
    """
    Prueba Unitaria (TDD): Verifica que el divisor de texto fragmente 
    correctamente un documento largo sin exceder el chunk_size.
    """
    # 1. Arrange (Preparar): Creamos un texto simulado de más de 1000 caracteres
    texto_largo = "La célula es la unidad fundamental de la vida. " * 50 
    
    # 2. Act (Actuar): Usamos la misma configuración de tu FaissAdapter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    fragmentos = text_splitter.split_text(texto_largo)
    
    # 3. Assert (Afirmar): Verificaciones estrictas
    # Verificamos que el texto efectivamente se dividió en más de 1 parte
    assert len(fragmentos) > 1, "El texto largo no se dividió en fragmentos."
    
    # Verificamos que NINGÚN fragmento supere los 500 caracteres
    for i, fragmento in enumerate(fragmentos):
        assert len(fragmento) <= 500, f"El fragmento {i} excedió el límite de 500 caracteres: tiene {len(fragmento)}"
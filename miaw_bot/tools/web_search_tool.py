from ddgs import DDGS

def web_search(query: str) -> str:
    """
    Busca información actualizada en internet mediante DuckDuckGo.
    Úsala cuando el usuario pregunte por noticias o datos recientes.
    """
    print(f"\n[Tool] 🌐 Buscando en la web: {query}...")
    try:
        # Extraemos los 3 primeros resultados
        resultados = DDGS().text(query, max_results=3)
        if not resultados:
            return "No se encontraron resultados en la web."

        formateado = ""
        for r in resultados:
            formateado += f"Título: {r['title']}\nTexto: {r['body']}\n\n"
        return formateado
    except Exception as e:
        return f"Error en la búsqueda web: {str(e)}"

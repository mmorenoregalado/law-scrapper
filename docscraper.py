from docx import Document
import re

def extract_articles(doc_path):
    # Abre el documento
    doc = Document(doc_path)

    # Inicializa un diccionario para guardar los artículos
    articles = {}

    # Inicializa las variables para almacenar el artículo actual y su texto
    current_article = None
    text = ""

    # Bandera para comprobar si hemos encontrado "ARTÍCULOS TRANSITORIOS"
    transitory_found = False

    # Recorre todos los párrafos en el documento
    for para in doc.paragraphs:
        # Comprueba si el párrafo es "ARTÍCULOS TRANSITORIOS"
        if para.text.strip() == "ARTÍCULOS TRANSITORIOS:":
            transitory_found = True

        # Si hemos encontrado "ARTÍCULOS TRANSITORIOS", ya no procesamos más párrafos
        if transitory_found:
            break

        # Comprueba si el párrafo comienza con "ARTÍCULO" seguido de un espacio
        if para.text.startswith("ARTÍCULO "):
            # Si hay un artículo actual, guarda su texto en el diccionario
            if current_article:
                articles[current_article] = text.strip()
            # Extrae solo la palabra "ARTÍCULO" y el número
            current_article = " ".join(para.text.split()[:2])
            # Inicia un nuevo texto para el artículo actual, removiendo el título del artículo
            text = " ".join(para.text.split()[2:])
        else:
            # Si no, agrega el párrafo al texto del artículo actual
            text += "\n" + para.text

    # Guarda el último artículo en el diccionario
    if current_article and not transitory_found:
        articles[current_article] = text.strip()

    return articles

# Ruta del documento .docx
doc_path = "130.docx"

# Llama a la función y muestra los resultados
articles = extract_articles(doc_path)
for article, text in articles.items():
    print(article)
    print(text)
    print("-------------")

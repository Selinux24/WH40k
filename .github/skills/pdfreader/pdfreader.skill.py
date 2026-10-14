import os
from pypdf import PdfReader

def leer_pdf_workspace(ruta_relativa_pdf):
    # Obtiene la ruta absoluta dentro de tu workspace de VS Code
    ruta_completa = os.path.abspath(ruta_relativa_pdf)
    
    if not os.path.exists(ruta_completa):
        return "Error: El archivo PDF no se encuentra en el workspace."
        
    lector = PdfReader(ruta_completa)
    texto_extraido = ""
    
    # Extrae el texto página por página
    for pagina in lector.pages:
        texto_extraido += pagina.extract_text() + "\n"
        
    return texto_extraido

import os
from bs4 import BeautifulSoup

class WebFileReader:
    def __init__(self, base_path="EjerciciosConHilos/Ejercicio04_WebScrapper/resources/input_html"):
        self.base_path = base_path

    def read_file(self, filename):
        """
        Lee un archivo HTML y devuelve su contenido como texto.
        """
        filepath = os.path.join(self.base_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"[WebFileReader] Archivo no encontrado: {filepath}")
            return None
        except Exception as e:
            print(f"[WebFileReader] Error al leer el archivo {filepath}: {str(e)}")
            return None
        
    def extract_links(self, html_content):
        """
        Extrae todos los enlaces de un contenido HTML dado.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links



import os
import threading
import queue
import time
from WebFileReader import WebFileReader

print("Directorio actual:", os.getcwd())

# Inicializa colas para la comunciación entre hilos
data_queue = queue.Queue()
link_queue = queue.Queue()

# Instancia de WebFileReader
reader = WebFileReader()

# Hilo A: Lee el archivos HTML y los coloca en data_queue
def hilo_a():
    filenames = ["index.html", "1.html", "2.html"]
    for filename in filenames:
        print(f"[Hilo A] Leyendo archivo: {filename}")
        content = reader.read_file(filename)
        if content:
            data_queue.put((filename, content))
        time.sleep(1) #Simulacion del tiempo de espera

# Hilo B: Extrae los enlaces del contenido HTML y los coloca en link_queue
def hilo_b():
    while True:
        if not data_queue.empty():
            filename, html_content = data_queue.get()
            print(f"[Hilo B] Extrayendo enlaces de: {filename}")
            links = reader.extract_links(html_content)
            for link in links:
                link_queue.put(link)

# Hilo C: Guarda el contenido de los archivos en archivos de texto en la carpeta resources
def hilo_c():
    while True:
        if not data_queue.empty():
            filename, html_content = data_queue.get()
            save_path = f"EjerciciosConHilos/Ejercicio04_WebScrapper/resources/output/{filename.replace('.html', '')}_content.txt"
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
                print(f"[Hilo C] Guardando contenido de {filename} en {save_path}")

# Hilo D: Guarda los enlaces extraídos en un archivo de texto para análisis
def hilo_d():
    while True:
        if not link_queue.empty():
            link = link_queue.get()
            with open("EjerciciosConHilos/Ejercicio04_WebScrapper/resources/output/extracted_links.txt", 'a', encoding='utf-8') as file:
                file.write(link + "\n")
            print(f"[Hilo D] Enlace guardado: {link}")

thread_a = threading.Thread(target=hilo_a, daemon=True)
thread_b = threading.Thread(target=hilo_b, daemon=True)
thread_c = threading.Thread(target=hilo_c, daemon=True)
thread_d = threading.Thread(target=hilo_d, daemon=True)

thread_a.start()
thread_b.start()
thread_c.start()
thread_d.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa terminado")
import os
import threading
import queue
from WebFileReader import WebFileReader

# Ruta base de los archivos HTML
base_path = "EjerciciosConHilos/Ejercicio04_WebScrapper/resources/input_html"
output_dir = "EjerciciosConHilos/Ejercicio04_WebScrapper/resources/output"
output_file = os.path.join(output_dir, "extracted_links.txt")

# Asegurarse de que la carpeta de salida existe
os.makedirs(output_dir, exist_ok=True)

# Cola de enlaces pendientes de procesar y conjunto de enlaces ya procesados
link_queue = queue.Queue()
processed_links = set()
lock = threading.Lock()  # Para sincronizar el acceso a `processed_links`

# Instancia de WebFileReader para leer HTML y extraer enlaces
reader = WebFileReader(base_path=base_path)

# Método adicional en WebFileReader para guardar los enlaces
def guardar_enlaces(enlaces):
    """
    Guarda los enlaces extraídos en un archivo.
    """
    with open(output_file, 'a', encoding='utf-8') as file:
        for enlace in enlaces:
            file.write(enlace + "\n")
    print(f"[WebFileReader] Enlaces guardados en {output_file}")

# Función que explora enlaces y descubre nuevos
def procesar_enlace():
    while True:
        # Obtener un enlace de la cola
        link = link_queue.get()
        
        # Si obtenemos None, significa que el procesamiento ha terminado
        if link is None:
            break

        # Marcar el enlace como procesado si no lo ha sido ya
        with lock:
            if link in processed_links:
                link_queue.task_done()
                continue
            processed_links.add(link)

        print(f"[Hilo] Procesando enlace: {link}")

        # Combinar `base_path` con el nombre del archivo para obtener la ruta completa
        full_path = os.path.join(base_path, link)
        
        # Leer el contenido del archivo HTML
        content = reader.read_file(link)
        if content:
            # Extraer los enlaces internos de este archivo
            new_links = reader.extract_links(content)
            
            # Guardar los enlaces extraídos
            guardar_enlaces(new_links)
            
            # Colocar nuevos enlaces en la cola si aún no han sido procesados
            for new_link in new_links:
                # Normalizar solo el nombre del archivo y agregar a la cola
                normalized_link = os.path.normpath(new_link)
                
                with lock:
                    if normalized_link not in processed_links:
                        link_queue.put(normalized_link)

        # Marcar este enlace como procesado en la cola
        link_queue.task_done()

# Enlace inicial para comenzar el procesamiento (solo nombre de archivo)
initial_link = "index.html"
link_queue.put(initial_link)

# Crear y lanzar los hilos para procesar los enlaces
num_threads = 4  # Ajusta el número de hilos según el sistema
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=procesar_enlace)
    thread.start()
    threads.append(thread)

# Esperar a que todos los enlaces en la cola se procesen
link_queue.join()

# Detener los hilos después de terminar el procesamiento
for _ in threads:
    link_queue.put(None)  # Insertar `None` para detener cada hilo

for thread in threads:
    thread.join()

print("Todos los enlaces han sido procesados.")

import requests
import urllib.parse
import json
import os
from typing import Dict, List, Any, Optional

# --- CONFIGURACIÓN CRÍTICA ---
# ¡IMPORTANTE! Reemplaza esta URL con la URL REAL de tu servicio FastAPI en Render.com.
# La encontrás en el dashboard de tu servicio en Render.
BASE_URL_FASTAPI = "https://gestor-audiencias-api.onrender.com" 
# Por ejemplo: https://gestor-audiencias-api.onrender.com

# --- FUNCIONES PARA INTERACTUAR CON TU API ---

def crear_archivo_excel_en_api(nombre_archivo: str) -> Dict[str, Any]:
    """
    Llama al endpoint /crear_archivo/ de tu FastAPI para crear una copia de la plantilla.
    """
    # Asegúrate de codificar el nombre del archivo para que sea seguro en la URL
    nombre_codificado = urllib.parse.quote_plus(nombre_archivo)
    url = f"{BASE_URL_FASTAPI}/crear_archivo/?nombre={nombre_codificado}"

    print(f"DEBUG: Llamando a la URL de creación de archivo: {url}") # Para depuración
    
    response = requests.post(url, headers={"Content-Type": "application/json"})
    try:
        response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"ERROR HTTP al crear archivo: {http_err}")
        try:
            error_detail = response.json().get('detail', response.text)
            print(f"Detalle del error desde API: {error_detail}")
        except json.JSONDecodeError:
            print(f"Respuesta del API (no JSON): {response.text}")
        raise
    except Exception as err:
        print(f"ERROR general al crear archivo: {err}")
        raise

def guardar_audiencia_en_api(datos_audiencia: Dict[str, Any]) -> Dict[str, Any]:
    """
    Llama al endpoint /audiencias/ de tu FastAPI para guardar una audiencia.
    """
    url = f"{BASE_URL_FASTAPI}/audiencias/"
    
    print(f"DEBUG: Llamando a la URL para guardar audiencia: {url}") # Para depuración
    print(f"DEBUG: Datos enviados: {datos_audiencia}") # Para depuración

    response = requests.post(url, json=datos_audiencia, headers={"Content-Type": "application/json"})
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"ERROR HTTP al guardar audiencia: {http_err}")
        try:
            error_detail = response.json().get('detail', response.text)
            print(f"Detalle del error desde API: {error_detail}")
        except json.JSONDecodeError:
            print(f"Respuesta del API (no JSON): {response.text}")
        raise
    except Exception as err:
        print(f"ERROR general al guardar audiencia: {err}")
        raise

def listar_archivos_en_api() -> List[Any]:
    """
    Llama al endpoint /archivos/ de tu FastAPI para listar los archivos existentes.
    """
    url = f"{BASE_URL_FASTAPI}/archivos/"
    
    print(f"DEBUG: Llamando a la URL para listar archivos: {url}") # Para depuración

    response = requests.get(url)
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"ERROR HTTP al listar archivos: {http_err}")
        try:
            error_detail = response.json().get('detail', response.text)
            print(f"Detalle del error desde API: {error_detail}")
        except json.JSONDecodeError:
            print(f"Respuesta del API (no JSON): {response.text}")
        raise
    except Exception as err:
        print(f"ERROR general al listar archivos: {err}")
        raise

def exportar_archivo_en_api(nombre_archivo: str) -> Dict[str, Any]:
    """
    Llama al endpoint /exportar/{nombre_archivo} de tu FastAPI para añadir firma.
    """
    nombre_codificado = urllib.parse.quote_plus(nombre_archivo)
    url = f"{BASE_URL_FASTAPI}/exportar/{nombre_codificado}"
    
    print(f"DEBUG: Llamando a la URL para exportar archivo: {url}") # Para depuración

    response = requests.post(url) # POST sin cuerpo para este endpoint
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"ERROR HTTP al exportar archivo: {http_err}")
        try:
            error_detail = response.json().get('detail', response.text)
            print(f"Detalle del error desde API: {error_detail}")
        except json.JSONDecodeError:
            print(f"Respuesta del API (no JSON): {response.text}")
        raise
    except Exception as err:
        print(f"ERROR general al exportar archivo: {err}")
        raise

def descargar_archivo_desde_api(nombre_archivo: str, ruta_guardado: str) -> str:
    """
    Llama al endpoint /descargar/{nombre_archivo} y guarda el archivo localmente.
    """
    nombre_codificado = urllib.parse.quote_plus(nombre_archivo)
    url = f"{BASE_URL_FASTAPI}/descargar/{nombre_codificado}"
    
    print(f"DEBUG: Llamando a la URL para descargar archivo: {url}") # Para depuración

    response: Optional[requests.Response] = None
    try:
        response = requests.get(url, stream=True) # stream=True para descargar archivos grandes
        response.raise_for_status()
        
        with open(ruta_guardado, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Archivo '{nombre_archivo}' descargado exitosamente en '{ruta_guardado}'")
        return ruta_guardado
    except requests.exceptions.HTTPError as http_err:
        print(f"ERROR HTTP al descargar archivo: {http_err}")
        # Si es un 404, el detalle podría estar en el cuerpo si FastAPI lo devuelve como JSON
        if response is not None and response.status_code == 404:
            try:
                error_detail = response.json().get('detail', response.text)
                print(f"Detalle del error desde API (404): {error_detail}")
            except json.JSONDecodeError:
                print(f"Respuesta del API (no JSON): {response.text}")
        raise
    except Exception as err:
        print(f"ERROR general al descargar archivo: {err}")
        raise

# --- EJEMPLO DE USO (cómo podrías usar estas funciones) ---
def main() -> None:
    """Función principal que ejecuta el ejemplo de uso."""
    nombre_excel_nuevo = "mi_informe_de_prueba.xlsx"

    # 1. Crear el archivo Excel (copia de la plantilla)
    try:
        print("\n--- Intentando crear archivo Excel ---")
        resultado_creacion = crear_archivo_excel_en_api(nombre_excel_nuevo)
        print(f"Resultado de creación: {resultado_creacion}")
    except Exception as e:
        print(f"No se pudo crear el archivo: {e}")
        # Si esto falla, no tiene sentido continuar, porque el archivo no existe.
        return

    # 2. Guardar una audiencia en el archivo recién creado
    datos_audiencia_ejemplo: Dict[str, Any] = {
        "radicado": "12345-ABC",
        "tipo_audiencia": "Conciliación",
        "fecha": "2024-07-25",
        "hora": "10:00",
        "juzgado": "Juzgado 1 Civil",
        "se_realizo": "Sí",
        "motivos": ["Acuerdo de partes"],
        "observaciones": "Audiencia exitosa"
    }
    # Asegúrate de pasar el nombre del archivo en el dict para guardar_audiencia_excel
    datos_audiencia_ejemplo["nombre_archivo"] = nombre_excel_nuevo

    try:
        print("\n--- Intentando guardar audiencia ---")
        resultado_guardado = guardar_audiencia_en_api(datos_audiencia_ejemplo)
        print(f"Resultado de guardado: {resultado_guardado}")
    except Exception as e:
        print(f"No se pudo guardar la audiencia: {e}")

    # 3. Listar archivos existentes
    try:
        print("\n--- Listando archivos ---")
        archivos_existentes = listar_archivos_en_api()
        print(f"Archivos en el servidor: {archivos_existentes}")
    except Exception as e:
        print(f"No se pudieron listar los archivos: {e}")

    # 4. Exportar el archivo (añadir firma)
    try:
        print("\n--- Intentando exportar archivo ---")
        resultado_exportacion = exportar_archivo_en_api(nombre_excel_nuevo)
        print(f"Resultado de exportación: {resultado_exportacion}")
        if "download_url" in resultado_exportacion:
            print(f"URL de descarga generada: {resultado_exportacion['download_url']}")
    except Exception as e:
        print(f"No se pudo exportar el archivo: {e}")

    # 5. Descargar el archivo exportado
    ruta_para_guardar_localmente = f"./descargas/{nombre_excel_nuevo}"
    os.makedirs("./descargas", exist_ok=True) # Asegura que la carpeta de descargas exista
    try:
        print("\n--- Intentando descargar archivo ---")
        ruta_descargada = descargar_archivo_desde_api(nombre_excel_nuevo, ruta_para_guardar_localmente)
        print(f"Archivo descargado en: {ruta_descargada}")
    except Exception as e:
        print(f"No se pudo descargar el archivo: {e}")

    # --- LLAMA A TU ENDPOINT DE DEPURACIÓN (MUY IMPORTANTE) ---
    print("\n--- Llamando al endpoint de depuración de archivos ---")
    print("¡COPIA LA RESPUESTA JSON DE ESTE ENDPOINT Y PÉGALA EN EL CHAT!")
    print("Esto es CRÍTICO para saber si tu plantilla está en Render.com.")
    try:
        # Aquí puedes llamar al debug endpoint directamente
        # En tu navegador sería: https://tu-url-de-fastapi-en-render.onrender.com/debug_archivos/
        # Para llamarlo desde Python y ver el JSON:
        debug_url = f"{BASE_URL_FASTAPI}/debug_archivos/"
        response_debug = requests.get(debug_url)
        response_debug.raise_for_status()
        print(f"Respuesta de /debug_archivos/: {json.dumps(response_debug.json(), indent=2)}")
    except Exception as e:
        print(f"Error al llamar a /debug_archivos/: {e}")

if __name__ == "__main__":
    main()
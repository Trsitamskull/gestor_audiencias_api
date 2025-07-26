from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import excel_utils
import os

app = FastAPI()

# Agrega este código después de crear la app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constante para la URL base
BASE_URL = "http://127.0.0.1:8000"

@app.post("/crear_archivo/")
def crear_archivo(nombre: str):
    try:
        # Asegura que termine en .xlsx
        if not nombre.endswith('.xlsx'):
            nombre += '.xlsx'
        
        ruta = excel_utils.crear_copia_plantilla(nombre)
        return {"ruta": ruta}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/audiencias/")
def guardar_audiencia(audiencia: dict):  # Ajusta según tu modelo Pydantic
    try:
        excel_utils.guardar_una_audiencia_excel(audiencia, audiencia["nombre_archivo"])
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/archivos/")
def listar():
    return excel_utils.listar_archivos()

@app.post("/exportar/{nombre_archivo}")
def exportar_archivo(nombre_archivo: str):
    """
    Exporta un archivo Excel con firma y devuelve la URL de descarga.
    
    Args:
        nombre_archivo: Nombre del archivo a exportar
        
    Returns:
        dict: Diccionario con la URL de descarga del archivo exportado
    """
    
    try:
        ruta_exportado = excel_utils.exportar_con_firma(nombre_archivo)
        nombre_archivo_exportado = os.path.basename(ruta_exportado)
        
        # Construye la URL de descarga
        download_url = f"{BASE_URL}/descargar/{nombre_archivo_exportado}"
        
        return {
            "download_url": download_url,
            "archivo_exportado": nombre_archivo_exportado
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/descargar/{nombre_archivo}")
def descargar_archivo(nombre_archivo: str):
    """
    Endpoint para descargar archivos exportados.
    
    Args:
        nombre_archivo: Nombre del archivo a descargar
        
    Returns:
        FileResponse: Archivo Excel para descarga
    """
    try:
        ruta_archivo = os.path.join(excel_utils.ARCHIVOS_DIR, nombre_archivo)
        
        if not os.path.exists(ruta_archivo):
            raise HTTPException(
                status_code=404, 
                detail=f"Archivo no encontrado: {nombre_archivo}"
            )
            
        return FileResponse(
            ruta_archivo,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=nombre_archivo
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
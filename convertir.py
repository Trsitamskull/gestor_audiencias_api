import base64
import os

def convertir_excel_a_base64(ruta_archivo):
    """
    Convierte un archivo Excel a string Base64 para embeber en código.
    
    Args:
        ruta_archivo (str): Ruta al archivo Excel a convertir
        
    Returns:
        str: String Base64 del archivo
    """
    
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")
    
    if not ruta_archivo.endswith(('.xlsx', '.xls')):
        raise ValueError("El archivo debe ser un Excel (.xlsx o .xls)")
    
    try:
        with open(ruta_archivo, "rb") as archivo_excel:
            # Codifica el contenido a Base64
            contenido_binario = archivo_excel.read()
            string_base64 = base64.b64encode(contenido_binario).decode('utf-8')
        
        # Muestra información del archivo
        tamaño_kb = len(contenido_binario) / 1024
        print(f"Archivo: {ruta_archivo}")
        print(f"Tamaño: {tamaño_kb:.2f} KB")
        print(f"Longitud del string Base64: {len(string_base64)} caracteres")
        print("\n" + "="*80)
        print("COPIA EL SIGUIENTE STRING COMPLETO (incluye las comillas):")
        print("="*80)
        print(f'"{string_base64}"')
        print("="*80)
        
        return string_base64
        
    except Exception as e:
        raise Exception(f"Error al procesar el archivo: {str(e)}")

# Uso del script
if __name__ == "__main__":
    # CAMBIA ESTA RUTA por la ubicación real de tu plantilla
    # Algunas opciones comunes:
    ruta_plantilla = "plantilla/plantilla_base.xlsx"  # Si tienes carpeta plantilla
    # ruta_plantilla = "plantilla_base.xlsx"  # Si está en la raíz del proyecto
    # ruta_plantilla = r"C:\ruta\completa\a\tu\plantilla_base.xlsx"  # Ruta absoluta
    
    try:
        string_base64 = convertir_excel_a_base64(ruta_plantilla)
        
        # Opcional: guardar en archivo de texto para fácil copia
        with open("plantilla_base64.txt", "w") as f:
            f.write(string_base64)
        print(f"\nTambién se guardó en: plantilla_base64.txt")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nAsegúrate de que:")
        print("1. El archivo 'plantilla/plantilla_base.xlsx' existe")
        print("2. Tienes permisos de lectura sobre el archivo")
        print("3. El archivo no está abierto en Excel u otro programa")
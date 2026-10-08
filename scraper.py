import requests
from bs4 import BeautifulSoup
import csv
import json
from pathlib import Path
from datetime import datetime

# Sandbox legal para pruebas de scraping
BASE_URL = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"

def fetch_html(url):
    """Realiza la petición HTTP y retorna el contenido HTML."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza error si la página no responde 200 OK
        return response.text
    except requests.RequestException as e:
        print(f"Error al conectar con la página: {e}")
        return None

def parse_products(html_content):
    """Extrae y limpia la información de los productos usando BeautifulSoup."""
    soup = BeautifulSoup(html_content, "html.parser")
    products = soup.find_all("article", class_="product_pod")
    
    extracted_data = []
    
    for item in products:
        # Extracción
        title = item.h3.a["title"]
        price_text = item.find("p", class_="price_color").text
        availability_text = item.find("p", class_="instock availability").text.strip()
        
        # Transformación y Limpieza
        # Convertimos el texto del precio (ej: "$23.23") a un número flotante útil
        clean_price = float(price_text.replace("£", "").strip())
        in_stock = "In stock" in availability_text
        
        extracted_data.append({
            "titulo": title,
            "precio": clean_price,
            "en_stock": in_stock,
            "fecha_extraccion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    return extracted_data

def generate_summary(data):
    """Calcula métricas simples a partir de los datos limpios."""
    if not data:
        return {}
    
    total_items = len(data)
    total_price = sum(item["precio"] for item in data)
    in_stock_count = sum(1 for item in data if item["en_stock"])
    
    return {
        "total_libros_extraidos": total_items,
        "precio_promedio": round(total_price / total_items, 2),
        "porcentaje_en_stock": round((in_stock_count / total_items) * 100, 2)
    }

def main():
    print(f"Iniciando extracción desde: {BASE_URL}")
    
    html = fetch_html(BASE_URL)
    if not html:
        return

    # Procesamiento de datos
    books_data = parse_products(html)
    print(f"Se extrajeron {len(books_data)} productos exitosamente.")

    # Creo carpeta de salida si no existe
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    # Exporto a CSV 
    csv_path = output_dir / "libros_extraidos.csv"
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["titulo", "precio", "en_stock", "fecha_extraccion"])
        writer.writeheader()
        writer.writerows(books_data)
    
    # Exporto Resumen a JSON 
    summary = generate_summary(books_data)
    json_path = output_dir / "resumen.json"
    with open(json_path, mode="w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)

    print(f"¡Proceso finalizado! Datos guardados en la carpeta '{output_dir}'.")

if __name__ == "__main__":
    main()

import os
import pandas as pd
import db.db as db 
import db.get_products as get_products

def get_info_db():
  CATEGORY_ENDPOINTS = [
        f"/api/catalog_system/pub/products/search?_from={start}&_to={start + 49}"
        for start in range(0, 5000, 50)
  ]

  BASE_URL = os.getenv("BASE_URL")
  if not BASE_URL:
      raise ValueError("BASE_URL no está configurado")
  all_products = []

  for endpoint in CATEGORY_ENDPOINTS:
      url = BASE_URL + endpoint
      products = get_products.get_products(url)
      if products:  # Verifica que no sea None o una lista vacía
          all_products.extend(products)

  if all_products:
      print(f"Se encontraron {len(all_products)} productos.")
      db.insert_products_into_db(all_products)
  else:
      print("No se encontraron productos.")

if __name__ == "__main__":
    get_info_db()
    print("Información de productos insertada en la base de datos.")
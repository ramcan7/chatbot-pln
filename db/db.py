import mysql.connector
import os
from config import DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT

def connect_to_database():
  return mysql.connector.connect(
      host=os.getenv("DB_HOST", DB_HOST),
      user=os.getenv("DB_USER", DB_USER),
      password=os.getenv("DB_PASSWORD", DB_PASS),
      database=os.getenv("DB_NAME", DB_NAME),
      port=os.getenv("DB_PORT", DB_PORT)
  )

def insert_products_into_db(products):
  connection = connect_to_database()
  cursor = connection.cursor()

  query = """
      INSERT INTO products (
          product_id, product_name, brand, price, list_price, measurement_unit,
          unit_multiplier, stock, category, promotions, payment_methods, link
      ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
      ON DUPLICATE KEY UPDATE
          product_name=VALUES(product_name),
          brand=VALUES(brand),
          price=VALUES(price),
          list_price=VALUES(list_price),
          measurement_unit=VALUES(measurement_unit),
          unit_multiplier=VALUES(unit_multiplier),
          stock=VALUES(stock),
          category=VALUES(category),
          promotions=VALUES(promotions),
          payment_methods=VALUES(payment_methods),
          link=VALUES(link)
  """

  cursor.executemany(query, products)
  connection.commit()
  print(f"{cursor.rowcount} productos insertados en la base de datos.")
  cursor.close()
  connection.close()
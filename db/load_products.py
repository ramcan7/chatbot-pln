import pandas as pd
import db.db as db

def load_products():
    conn = db.connect_to_database()
    df = pd.read_sql("SELECT * FROM products;", conn)
    conn.close()
    return df


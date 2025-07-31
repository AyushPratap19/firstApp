
import sqlite3
import pandas as pd

def load_data():
    conn = sqlite3.connect('products.db')
    df = pd.read_csv('product.csv')
    df.to_sql('products', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    return df.to_dict(orient='records')

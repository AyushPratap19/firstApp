from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Product
import pandas as pd
import os

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')

db.init_app(app)

def load_csv_to_db():
    with app.app_context():
        db.create_all()
        # Prevent duplicate entries
        if Product.query.first():
            return
        if os.path.exists("products.csv"):
            df = pd.read_csv("products.csv")
            for _, row in df.iterrows():
                product = Product(
                    id=row['id'],
                    cost=row['cost'],
                    category=row['category'],
                    name=row['name'],
                    brand=row['brand'],
                    retail_price=row['retail_price'],
                    department=row['department'],
                    sku=row['sku'],
                    distribution_center_id=row['distribution_center_id']
                )
                db.session.add(product)
            db.session.commit()

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        load_csv_to_db()
    app.run(debug=True)

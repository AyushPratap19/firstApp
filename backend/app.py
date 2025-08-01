from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Product, Department
import pandas as pd
import os

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')

db.init_app(app)

def load_csv_to_db():
    with app.app_context():
        db.create_all()

        if Product.query.first():
            return

        if os.path.exists("products.csv"):
            df = pd.read_csv("products.csv")

            # Create unique departments
            departments = df['department'].dropna().unique()
            dept_map = {}
            for dept_name in departments:
                dept = Department(name=dept_name)
                db.session.add(dept)
                db.session.flush()  # to get ID before commit
                dept_map[dept_name] = dept.id

            # Add products
            for _, row in df.iterrows():
                dept_id = dept_map.get(row['department'])
                product = Product(
                    id=row['id'],
                    cost=row['cost'],
                    category=row['category'],
                    name=row['name'],
                    brand=row['brand'],
                    retail_price=row['retail_price'],
                    department_id=dept_id,
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

@app.route('/api/departments', methods=['GET'])
def get_departments():
        departments = Department.query.all()
        result = []
        for dept in departments:
         product_count = Product.query.filter_by(department_id=dept.id).count()
        result.append({
            'id': dept.id,
            'name': dept.name,
            'product_count': product_count
        })
        return jsonify(result), 200

@app.route('/api/departments/<int:id>', methods=['GET'])
def get_department(id):
    department = Department.query.get(id)
    if not department:
        return jsonify({'error': 'Department not found'}), 404
    return jsonify({'id': department.id, 'name': department.name}), 200

@app.route('/api/departments/<int:id>/products', methods=['GET'])
def get_department_products(id):
    department = Department.query.get(id)
    if not department:
        return jsonify({'error': 'Department not found'}), 404

    products = Product.query.filter_by(department_id=id).all()
    product_list = [{
        'id': product.id,
        'name': product.name,
        'brand': product.brand,
        'price': product.retail_price
    } for product in products]

    return jsonify({'department': department.name, 'products': product_list}), 200


if __name__ == '__main__':
    with app.app_context():
        load_csv_to_db()
    app.run(debug=True)

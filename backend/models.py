# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float)
    category = db.Column(db.String(100))
    name = db.Column(db.String(255))
    brand = db.Column(db.String(100))
    retail_price = db.Column(db.Float)
    department = db.Column(db.String(100))
    sku = db.Column(db.String(100))
    distribution_center_id = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'cost': self.cost,
            'category': self.category,
            'name': self.name,
            'brand': self.brand,
            'retail_price': self.retail_price,
            'department': self.department,
            'sku': self.sku,
            'distribution_center_id': self.distribution_center_id
        }



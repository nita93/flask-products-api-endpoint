from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Init db
db = SQLAlchemy(app)

api.app.config['RESTFUL_JSON'] = {
    'ensure_ascii': False
}

class Image(db.Model):
    key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String(200), db.ForeignKey('product.id'))
    link = db.Column(db.String(300))

    def __init__(self, product_id, link):
        self.product_id = product_id
        self.link = link

class Product(db.Model):
    key = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000))
    category = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    oldPrice = db.Column(db.Float(), nullable=False)
    brand = db.Column(db.String(200))
    parentCategory = db.Column(db.String(200))
    color = db.Column(db.String(50))

    image = db.relationship('Image', backref='product')

    def __init__(self, id, name, description, category, link, price, oldPrice, brand, parentCategory, color):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.link = link
        self.price = price
        self.oldPrice = oldPrice
        self.brand = brand
        self.parentCategory = parentCategory
        self.color = color

image_fields = {
    'link': fields.String
}

resource_fields = {
    'id': fields.String,
    'name': fields.String,
    'description': fields.String,
    'category': fields.String,
    'link': fields.String,
    'price': fields.Float,
    'oldPrice': fields.Float,
    'brand': fields.String,
    'color': fields.String,
    'image': fields.List(fields.String(attribute="link"))
}

class Offer(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = request.args
        category_name = args.get('category')
        parent_category_name = args.get('parent')
        if parent_category_name:
            results = Product.query.filter_by(parentCategory=parent_category_name).all()
        elif category_name:
            results = Product.query.filter_by(category=category_name).all()
        else:
            results = Product.query.filter_by().all()
        return results

api.add_resource(Offer, "/api")

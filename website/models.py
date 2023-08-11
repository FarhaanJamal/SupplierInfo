from . import db
from flask_login import UserMixin

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplierName = db.Column(db.String(1500))
    amount = db.Column(db.Integer)
    itemId = db.Column(db.Integer, db.ForeignKey("item.id"))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(3000), unique=True)
    #picture
    suppliers = db.relationship("Supplier")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Item, Supplier
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    global current_item
    current_item = "{}"
    itemName = ""
    if request.method == "POST":
        itemName = request.form.get("search").lower()
        item = Item.query.filter_by(itemName=itemName).first()
        if item:
            current_item = item
            flash("Successful retrival.", category="success")
        else:
            flash("Item does not exist.", category="error")
    return render_template("home.html", user=current_user, item=current_item, itemName=itemName)

@views.route('/insert', methods=["GET", "POST"])
@login_required
def insert():
    if request.method == "POST":
        itemName = request.form.get("itemName").lower()
        supplierName = request.form.get("supplierName").lower()
        amount = request.form.get("amount")

        item = Item.query.filter_by(itemName=itemName).first()
        
        if len(itemName) < 1:
            flash("Item name is too short.", category="error")
        elif len(supplierName) < 1:
            flash("Supplier name is too short.", category="error")
        elif len(amount) < 1:
            flash("Amount can't be empty.", category="error")
        elif amount == "-1000":
            while True:
                supplier = Supplier.query.filter_by(itemId=item.id).first()
                if supplier:
                    db.session.delete(supplier)
                    db.session.commit()
                else:
                    break
            db.session.delete(item)
            db.session.commit()
            flash("Item succesfully deleted.", category="success")
        elif amount == "-1001":
            supplier = Supplier.query.filter_by(supplierName=supplierName, itemId=item.id).first()
            if supplier:
                db.session.delete(supplier)
                db.session.commit()
                flash("Supplier succesfully deleted.", category="success")
            else:
                flash("Supplier does not exist.", category="error")
        elif amount[0] == "-":
            flash("Amount can't be negative.", category="error")
        elif item:
            supplier = Supplier.query.filter_by(supplierName=supplierName, amount=amount, itemId=item.id).first()
            if supplier:
                flash("This supplier already exist for this item with the same amount", category="error")
            else:
                flag = False
                supplier = Supplier.query.filter_by(supplierName=supplierName, itemId=item.id).first()
                if supplier:
                    db.session.delete(supplier)
                    db.session.commit()
                    flag = True
                new_supplier = Supplier(supplierName=supplierName, amount=amount, itemId=item.id)
                db.session.add(new_supplier)
                db.session.commit()
                if flag:
                    flash("Suppliers amount edited", category="success")
                else:
                    flash("New supplier successfully added", category="success")
        else:
            new_item = Item(itemName=itemName)
            db.session.add(new_item)
            db.session.commit()
            item = new_item

            new_supplier = Supplier(supplierName=supplierName, amount=amount, itemId=item.id)
            db.session.add(new_supplier)
            db.session.commit()
            flash("New item with supplier successfully added", category="success")

    return render_template("insert.html", user=current_user)
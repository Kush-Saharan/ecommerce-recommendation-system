# routes/products.py
from flask import Blueprint, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from app.models.product import Product, db

product_bp = Blueprint('product', __name__)

@product_bp.route('/product')
def view_products():
    all_products = Product.query.all()
    return render_template('product.html', products=all_products)

@product_bp.route('/')
def home():
    return render_template('index.html')
# routes/products.py
from flask import Blueprint, render_template,request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from app.models.product import Product, db

product_bp = Blueprint('product', __name__)

@product_bp.route('/product')
@login_required
def view_products():
    all_products = Product.query.all()
    return render_template('product.html', products=all_products)

@product_bp.route('/search',methods=['GET'])
@login_required
def search_products():
    name = request.args.get('query')
    products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
    return render_template('index.html',products=products)



@product_bp.route('/')
@login_required
def home():
    all_products = Product.query.all()
    return render_template('index.html', products=all_products)
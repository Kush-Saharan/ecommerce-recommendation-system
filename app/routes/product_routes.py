# routes/products.py
from flask import Blueprint, render_template,request,redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from app.models.product import Product, db
from app.models.user_cart import Cart
from app.models.order import Order

product_bp = Blueprint('product', __name__)

@product_bp.route('/product')
@login_required
def view_products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@product_bp.route('/search',methods=['GET'])
@login_required
def search_products():
    name = request.args.get('query')
    products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
    return render_template('index.html',products=products)

@product_bp.route('/product/<int:id>')
@login_required
def product_details(id):
    product=Product.query.filter_by(id=id).first()
    return render_template('product_details.html',product=product)

@product_bp.route('/product/buy/<int:id>')
@login_required
def product_buy(id):
    product=Product.query.filter_by(id=id).first()
    if product.quantity>=1:
        product.quantity -= 1
        user_id=current_user.id
        product_id=id
        total_price=product.price
        order=Order(user_id=user_id,product_id=product_id,total_price=total_price,)
        message="Product Bought!"
        db.session.add(order)
        db.session.commit()
    else:
        message="The product is unavailable right now."
        
    return render_template('product_details.html',message=message,product=product)

@product_bp.route("/user/cart", methods=['POST','GET'])
@login_required
def product_user_cart():
    if request.method=='POST':
        pass
    else:
        user_id=current_user.id
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        return render_template('user_cart.html',cart_items=cart_items,total_amount=total_amount)
    
@product_bp.route("/checkout",methods=['POST','GET'])
@login_required
def checkout():
    user_id=current_user.id
    cart_items=Cart.query.filter_by(user_id=user_id).all()
    for cart_item in cart_items:
        product=Product.query.filter_by(id=cart_item.product_id).first()
        if product.quantity>=cart_item.quantity:
            order=Order(user_id=user_id,product_id=product.id,total_price=product.price*cart_item.quantity)
            db.session.add(order)
            product.quantity -= cart_item.quantity
        else:
            message = f"Product '{product.name}' is out of stock or insufficient quantity."
            return render_template('user_cart.html', cart_items=cart_items, message=message)
    db.session.commit()

    for cart_item in cart_items:
        db.session.delete(cart_item)
    db.session.commit()

    cart_items = Cart.query.filter_by(user_id=user_id).all()

    message="Products Bought successfully"

    return render_template('user_cart.html',cart_items=cart_items,message=message)

@product_bp.route('/product/cart/<int:id>')
@login_required
def product_cart(id):
    product_id=id
    user_id=current_user.id
    product_current=Cart.query.filter_by(product_id=product_id,user_id=user_id).first()
    if product_current:
        quantity=product_current.quantity+1
        product_current.quantity=quantity
        message="Product quantity updated to cart successfully"
    else:
        product_current=Cart(product_id=product_id,user_id=user_id,quantity=1)
        db.session.add(product_current)
        message="Product added to cart successfully"
    
    db.session.commit()
    product=Product.query.filter_by(id=product_id).first()

    return render_template('product_details.html',product=product,message=message)

@product_bp.route('/cart/delete/<int:id>')
@login_required
def remove_item(id):
    user_id = current_user.id
    cart_items = Cart.query.filter_by(user_id=user_id, id=id).all()
    
    if not cart_items:
        message = "Item not found in your cart."
    else:
        for item in cart_items:
            db.session.delete(item)
        db.session.commit()
        message = "Removed item successfully"

    updated_cart = Cart.query.filter_by(user_id=user_id).all()
    return render_template('user_cart.html', cart_items=updated_cart, message=message)


@product_bp.route('/')
@login_required
def home():
    all_products = Product.query.all()
    return render_template('index.html', products=all_products)
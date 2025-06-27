from flask import render_template,redirect,abort,Blueprint,request
from flask_login import current_user,login_required,login_user,logout_user
from app.models.user import User
from app.main import login_manager,db
from app.models.product import Product

admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        check_user=User.query.filter_by(email=email,password=password).first()
        if check_user:
            if check_user.role =='admin':
                login_user(check_user)
                return redirect('/admin/dashboard')
            else:
                return render_template('admin/admin_login.html', error_admin_login="Not an admin")

        else:
            return render_template('/admin/admin_login.html', error_admin_login="Invalid login or password")
    return render_template('/admin/admin_login.html')

@admin_bp.route('/admin/dashboard',methods=['POST','GET'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)
    else:
        return render_template('/admin/admin_dashboard.html')
    
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')
    
@admin_bp.route('/admin/products/add',methods=['POST','GET'])
@login_required
def add_products():
    if current_user.role != 'admin':
        abort(403)

    if request.method=='POST':
        name=request.form['name']
        description=request.form['description']
        price=request.form['price']
        category=request.form['category']
        brand=request.form['brand']
        quantity=request.form['quantity']

        existing_product=Product.query.filter_by(name=name,brand=brand).first()

        if existing_product:
            existing_product.price=price
            existing_product.description=description
            existing_product.category=category
            existing_product.quantity+=int(quantity)
            message="Product updated successfully"
        else:
            new_product=Product(name=name,description=description,price=price,brand=brand,category=category,quantity=quantity)
            db.session.add(new_product)
            message="Product added successfully"
        
        db.session.commit()
        return render_template('/admin/admin_products_add.html',message=message)
        
    return render_template('/admin/admin_products_add.html')

@admin_bp.route('/admin/product/search',methods=['GET'])
@login_required
def search_products():
    name = request.args.get('query')
    products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
    return render_template('/admin/admin_products.html',products=products)

@admin_bp.route('/admin/products')
@login_required
def view_products():
    all_products = Product.query.all()
    return render_template('/admin/admin_products.html', products=all_products)

@admin_bp.route('/admin/product/edit/<int:id>',methods=['POST','GET'])
@login_required
def edit_products(id):

    if request.method=='POST':

        product = Product.query.get_or_404(id)

        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.category = request.form['category']
        product.brand = request.form['brand']
        product.quantity=request.form['quantity']

        message="Product edited successfully"

        db.session.commit()
        return render_template('/admin/admin_products.html',message=message)
    
    else:
        product=Product.query.filter_by(id=id).first()
        return render_template('/admin/admin_products_edit.html',product=product)

@admin_bp.route('/admin/product/delete/<int:id>', methods=['GET'])
@login_required
def delete_products(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    message="Product deleted successfully"
    return render_template('/admin/admin_products.html',message=message,product=product)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



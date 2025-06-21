from flask import Blueprint, request, jsonify,render_template,redirect,abort
from app.models.user import User
from app.main import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST','GET'])
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error_Register="Username already taken")
        elif User.query.filter_by(email=email).first():
            return render_template('register.html', error_Register="Email already registered")
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        
    return render_template('register.html')

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        check_user=User.query.filter_by(email=email,password=password).first()
        if check_user:
            return redirect('/')
        else:
            return render_template('login.html', error_Login="Inavlid login or password")
    return render_template('login.html')

@auth_bp.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        check_user=User.query.filter_by(email=email,password=password).first()
        if check_user:
            if check_user.role()=='admin':
                return redirect('/admin/dashboard')
        else:
            return render_template('admin_login.html', error_Login="Inavlid login or password")
    return render_template('admin_login.html')


from flask import Blueprint, request,render_template,redirect,abort
from app.models.user import User
from app.main import db
from flask_login import login_user,login_required,logout_user
from app.main import login_manager

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
            login_user(check_user)
            return redirect('/')
        else:
            return render_template('login.html', error_Login="Inavlid login or password")
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


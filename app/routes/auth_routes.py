from flask import Blueprint, request, jsonify,render_template,redirect
from app.models.user import User
from app.main import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST','GET'])
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"})
    return render_template('register.html')

@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        check_user=User.query.filter_by(email=email,password=password).first()
        if check_user:
            return redirect('/')
    return render_template('login.html')

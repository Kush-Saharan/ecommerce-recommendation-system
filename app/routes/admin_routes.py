from flask import render_template,redirect,abort,Blueprint,request
from flask_login import current_user
from app.models.user import User
from app.main import db

admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        check_user=User.query.filter_by(email=email,password=password).first()
        if check_user:
            if check_user.role()=='admin':
                return redirect('/admin/dashboard')
        else:
            return render_template('admin_login.html', error_Login="Invalid login or password")
    return render_template('admin_login.html')

@admin_bp.route('/admin/dashboard',methods=['POST','GET'])
def admin_dashboard():
    if current_user.role()!='admin':
        abort(403)
    return render_template('admin_dashboard.html')


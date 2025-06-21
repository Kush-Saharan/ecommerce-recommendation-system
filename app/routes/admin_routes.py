from flask import render_template,redirect,abort,Blueprint,request
from flask_login import current_user,login_required,login_user,logout_user
from app.models.user import User
from app.main import login_manager

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
                return render_template('admin_login.html', error_admin_login="Not an admin")

        else:
            return render_template('admin_login.html', error_admin_login="Invalid login or password")
    return render_template('admin_login.html')

@admin_bp.route('/admin/dashboard',methods=['POST','GET'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)
    else:
        return render_template('admin_dashboard.html')
    
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()       #initialises database
login_manager = LoginManager()      #necessary for many flask_login commands

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'     #makes the database named site.db
    app.config['SECRET_KEY'] = 'SomethingRandom'        #necessary for many flask_login commands
    db.init_app(app)    

    login_manager.init_app(app)

    from app.routes.auth_routes import auth_bp      #accesses the blueprint from the files which is basically path
    from app.routes.product_routes import product_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)     #the blueprints are registered here
    app.register_blueprint(product_bp)
    app.register_blueprint(admin_bp)
    
    return app

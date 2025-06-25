from app.main import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    order_id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
    total_price=db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='orders')
    product = db.relationship('Product')
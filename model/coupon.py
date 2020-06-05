from model import db

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coupon_code = db.Column(db.String(28), unique=True, nullable=False)
    coupon_status = db.Column(db.String(20), nullable=False)
    bind_user_id = db.Column(db.String(20), nullable=True)
    expire_date = db.Column(db.String(8), nullable=False)
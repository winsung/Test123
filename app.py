from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager

from model import db
from endpoint import api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///coupon_service.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = 'flask_jwt_kay'

jwt = JWTManager(app)
db.init_app(app)
api.init_app(app)

with app.app_context():
    db.create_all()

def init_db():
    with app.app_context():
        db.session.commit()
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
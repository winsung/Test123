from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager

from model import db
from endpoint import api

import threading
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///coupon_service.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = 'flask_jwt_kay'

jwt = JWTManager(app)
db.init_app(app)
api.init_app(app)

def expire_checker_thread_timer_func(last_ymd):
    with app.app_context():
        th = None
        expire_date = datetime.datetime.now() + datetime.timedelta(days=3)
        expire_date = expire_date.strftime("%Y%m%d")
        if last_ymd != expire_date:
            from model.coupon import Coupon
            res = Coupon.query.filter_by(expire_date=expire_date).all()
            for item in res:
                if item.bind_user_id:
                    print("{}, Your coupon ({}) expire in 3 days.".format(item.bind_user_id, item.coupon_code))
            
            th = threading.Timer(interval=60*60*24, function=expire_checker_thread_timer_func, args=(expire_date,))
        else:
            th = threading.Timer(interval=60*60, function=expire_checker_thread_timer_func, args=(last_ymd,))
        th.daemon = True
        th.start()

with app.app_context():
    db.create_all()
    expire_date = datetime.datetime.now() + datetime.timedelta(days=3)
    expire_date = expire_date.strftime("%Y%m%d")
    expire_checker_thread_timer_func(expire_date)

def init_db():
    with app.app_context():
        db.session.commit()
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
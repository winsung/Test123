from flask import request
from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import jwt_required

from model import db
from model.coupon import Coupon
from model.user import User

import uuid
import datetime

api = Namespace('coupon', description="coupon")

coupon_bind_model = api.model("coupon_bind", {
    'coupon_code': fields.String(required=True),
    'user_id': fields.String(required=True)
})

@api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
@api.route('')
class CouponManagement(Resource):
    @api.expect(api.model('coupon_create', {'create_count': fields.Integer(required=True)}))
    @jwt_required
    def post(self):
        """
        create coupons
        """
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        create_count = request.json.get('create_count', None)
        if not create_count:
            return {"msg": "Missing create_count parameter"}, 400
        
        for _ in range(create_count):
            # use uuid for coupon code
            coupon_code = 'kakaopay' + str(uuid.uuid4())[8:28] # mytest01-xxxx-xxxx-xxxx-xxxx
            expire_date = datetime.datetime.now() + datetime.timedelta(days=7) # expire day default: after 7 days
            expire_date = expire_date.strftime("%Y%m%d")
            # status: CREATED, USED
            coupon = Coupon(
                coupon_code=coupon_code,
                coupon_status="CREATED",
                expire_date=expire_date
            )
            
            db.session.add(coupon)
        result = db.session.commit()

        return {"msg": "{} Coupon Created.".format(create_count)}, 200
    
    @api.expect(coupon_bind_model)
    @jwt_required
    def put(self):
        """
        bind coupon to user
        """
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        coupon_code = request.json.get('coupon_code', None)
        user_id = request.json.get('user_id', None)
        if not coupon_code:
            return {"msg": "Missing coupon_code parameter"}, 400

        if not user_id:
            return {"msg": "Missing user_id parameter"}, 400

        coupon_res = Coupon.query.filter_by(coupon_code=coupon_code).first()
        if not coupon_res:
            return {"msg": "{} not exists.".format(coupon_code)}, 401
        
        if coupon_res.coupon_status == "USED":
            return {"msg": "{} cannot be bind. It's already USED.".format(coupon_code)}, 400
        
        if coupon_res.bind_user_id:
            return {"msg": "{} is already bind to {}".format(coupon_code, coupon_res.bind_user_id)}

        user_res = User.query.filter_by(user_id=user_id).first()
        if not user_res:
            return {"msg": "User not found"}, 401
        
        try:
            coupon_res.bind_user_id = user_id
            db.session.commit()
        except Exception as ex:
            return {"msg": "coupon bind update error!!"}, 500

        return {"msg": "{} is successfully bind to {}".format(coupon_code, user_id)}


    def get(self):
        """
        show all coupon list
        """
        result = Coupon.query.all()
        ret_list = []
        for coupon in result:
            ret_list.append(coupon.coupon_code)

        return {"coupon_list": ret_list}, 200

@api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
@api.route('/bind_list')
class CouponBindList(Resource):
    @jwt_required
    def get(self):
        """
        show bind coupon list
        """
        result = Coupon.query.filter((Coupon.bind_user_id != None) | (Coupon.bind_user_id != "")).all()
        ret_list = []
        for coupon in result:
            body = {
                "coupon_code": coupon.coupon_code,
                "bind_user_id": coupon.bind_user_id,
                "expire_date": coupon.expire_date
            }
            ret_list.append(body)

        return {"bind_coupon_list": ret_list}, 200

@api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
@api.route('/use')
class CouponUse(Resource):
    @jwt_required
    @api.expect(api.model('coupon_use', {'coupon_code': fields.String(required=True)}))
    def post(self):
        """
        use coupon
        """
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        coupon_code = request.json.get('coupon_code', None)
        if not coupon_code:
            return {"msg": "Missing coupon_code parameter"}, 400
        
        coupon_res = Coupon.query.filter_by(coupon_code=coupon_code).first()
        if not coupon_res:
            return {"msg": "{} not exists.".format(coupon_code)}, 401
        
        if coupon_res.coupon_status == "USED":
            return {"msg": "{} cannot use. It's already USED.".format(coupon_code)}, 400
        
        try:
            coupon_res.coupon_status = "USED"
            db.session.commit()
        except Exception as ex:
            return {"msg": "coupon use update error!!"}, 500
        
        return {"msg": "{} is successfully used".format(coupon_code)}

        

@api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
@api.route('/cancel/<coupon_code>')
class CouponUseCancel(Resource):
    @jwt_required
    def post(self, coupon_code):
        """
        used coupon cancel
        """
        result = Coupon.query.filter_by(coupon_code=coupon_code).first()
        if not result:
            return {"msg": "{} not exists.".format(coupon_code)}, 401
        
        if not result.coupon_status == "USED":
            return {"msg": "{} is not used. status={}".format(coupon_code, result.coupon_status)}, 400

        try:
            result.coupon_status = "CREATED"
            db.session.commit()
        except Exception as ex:
            return {"msg": "coupon cancel update error!!"}, 500

        return {"msg": "{}'s status is successfully canceled".format(coupon_code)}, 200

@api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
@api.route('/expired-today')
class CouponExpired(Resource):
    @jwt_required
    def get(self):
        """
        show coupon list which is expired today
        """
        today_ymd = datetime.datetime.now().strftime("%Y%m%d")
        result = Coupon.query.filter_by(expire_date=today_ymd).all()

        ret_list = []
        for item in result:
            body = {
                "coupon_code": item.coupon_code,
                "coupon_status": item.coupon_status,
                "bind_user_id": item.bind_user_id
            }
            ret_list.append(body)

        return {"result": ret_list}

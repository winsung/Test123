from flask import request
from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from model import db
from model.user import User

import datetime
import bcrypt

api = Namespace('user', description="user")

user_login_model = api.model('User', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/signup')
class UserSignup(Resource):
    @api.expect(user_login_model, validate=True)
    def post(self):
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return {"msg": "Missing username parameter"}, 400
        if not password:
            return {"msg": "Missing password parameter"}, 400

        # encrypt password using bcrypt
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(user_id=username, password=password)
        db.session.add(user)
        db.session.commit()

        return {"msg": "{} sign up".format(username)}, 200
    

@api.route('/login')
class UserAPI(Resource):
    @api.expect(user_login_model, validate=True)
    def post(self):
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return {"msg": "Missing username parameter"}, 400
        if not password:
            return {"msg": "Missing password parameter"}, 400

        user = User.query.filter_by(user_id=username).first()
        if not user:
            return {"msg": "User not found"}, 401
        
        if not bcrypt.checkpw(password.encode('utf-8'), user.password): 
            return {"msg": "Bad password"}, 401

        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=username, expires_delta=expires)
        return {"access_token": access_token}, 200

@api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
@api.route('/jwt_test')
class JWTTestAPI(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        return {"logged_in_as": current_user}, 200

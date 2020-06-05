from flask_restplus import Api

from .user_api import api as ns_user
from .coupon_api import api as ns_coupon

authorizations = {
    'apikey' : {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token. ex) Bearer xxxxxx"
    }
}

api = Api(
    title="Kakaopay Pre-Test, Coupon Service",
    version="1.0",
    description="REST API for Coupon Service using flask (python)",
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(ns_user)
api.add_namespace(ns_coupon)

# Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTEzNTYyNjEsIm5iZiI6MTU5MTM1NjI2MSwianRpIjoiYWJjNzI3NTMtOWQ1MS00ZWE5LTg1NjgtMDdmMTQwNmUyNWZjIiwiZXhwIjoxNTkxNDQyNjYxLCJpZGVudGl0eSI6ImFkbWluIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.3a7o47uWYmAegEBn26L30DIivReCcib4I0uwYXKhVks
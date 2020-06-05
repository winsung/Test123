import unittest

from app import app, init_db, db
from model.coupon import Coupon

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///unittest.db'
init_db()

class UserAndJWTTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_1_signup_and_login_and_jwt(self):
        rv = self.app.post(
            '/user/signup', 
            content_type='application/json', 
            json={
                'username': 'test1',
                'password': 'test1234'
            })
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('sign up' in rv.get_json()['msg'])
    
        rv = self.app.post(
            '/user/login', 
            content_type='application/json', 
            json={
                'username': 'test1',
                'password': 'test1234'
            })
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('access_token' in rv.get_json())
        token = rv.get_json()['access_token']
        self.assertIsNotNone(token)
        
        header = {
            'Authorization': 'Bearer {}'.format(token)
        }
        rv = self.app.get(
            '/user/jwt_test',
            headers=header
        )
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.get_json()["logged_in_as"], "test1")

class CouponTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.post(
            '/user/signup', 
            content_type='application/json', 
            json={
                'username': 'test2',
                'password': 'test222'
            })

        self.token = self.app.post(
            '/user/login', 
            content_type='application/json', 
            json={
                'username': 'test2',
                'password': 'test222'
            }
        ).get_json()['access_token']
        self.header = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
    
    def test_1_coupon_create_and_bind_and_get_bind_list(self):
        rv = self.app.post(
            '/coupon',
            headers=self.header,
            json={
                'create_count': 100
            }
        )
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('Coupon Created.' in rv.get_json()['msg'])

        coupon_list = self.app.get('/coupon').get_json()['coupon_list']
        for code in coupon_list[:10]:
            rv = self.app.put(
                '/coupon',
                headers=self.header,
                json={
                    'coupon_code': code,
                    'user_id': 'test2'
                }
            )
            self.assertEqual(rv.status_code, 200)
            self.assertTrue('is successfully bind to' in rv.get_json()['msg'])
    
        rv = self.app.get('/coupon/bind_list', headers=self.header)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(len(rv.get_json()['bind_coupon_list']), 10)

    def test_2_coupon_use_and_cancel_and_get_expire_list(self):
        coupon_list = self.app.get('/coupon').get_json()['coupon_list']

        rv = self.app.post(
            '/coupon/use',
            headers=self.header,
            json={
                'coupon_code': coupon_list[0]
            }
        )
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('is successfully used' in rv.get_json()['msg'])

        rv = self.app.post(
            '/coupon/cancel/{}'.format(coupon_list[0]),
            headers=self.header
        )
        self.assertEqual(rv.status_code, 200)
        self.assertTrue('status is successfully canceled' in rv.get_json()['msg'])

        import datetime
        today_ymd = datetime.datetime.now().strftime("%Y%m%d")
        rv = self.app.get('/coupon/expired-today', headers=self.header)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(len(rv.get_json()['result']), 0)


if __name__ == '__main__':
    unittest.main()
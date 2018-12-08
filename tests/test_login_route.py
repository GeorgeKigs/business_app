from customer_data import customer_data,db,bcrypt
import unittest
from customer_data.database import Users,Companies
from random import randint

class Login_route_test(unittest.TestCase):
    def setUp(self):
        customer_data.config['TESTING']=True
        customer_data.config['WTF_CSRF_ENABLED']=False
       
    def tearDown(self):
        pass


    def test_login(self):
        tester=customer_data.test_client(self)
        response=tester.get('/auth/login/',content_type='html/text')
        self.assertEqual(response.status_code,200)

    def test_login_loads(self):
        tester=customer_data.test_client(self)
        response=tester.get('/auth/login/',content_type='html/text')
        self.assertTrue(b'Email' in response.data)
    
    def test_login_correct_credentials(self,email,password,follow):
        tester=customer_data.test_client(self)
        return tester.post('/auth/login/',
            data=dict(email=email,
            password=password),
            follow_redirects=follow
            )

    def test_invalid_user(self):
        response=self.test_login_correct_credentials('gk@g.com','pass7word',False)
        self.assertIn(b"enter the right credentials",response.data)

    def test_no_details(self):
        response=self.test_login_correct_credentials('','',False)
        self.assertIn(b"This field is required",response.data)
        

    def test_valid_user(self):
        response=self.test_login_correct_credentials('gk@g.com','password',True)
        self.assertEqual(response.status_code,302)
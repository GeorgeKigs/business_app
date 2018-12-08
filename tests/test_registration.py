from customer_data import customer_data,db,bcrypt
import unittest
from customer_data.database import Users,Companies
from random import randint

class Registration_route_test(unittest.TestCase):
    def setUp(self):
        customer_data.config['TESTING']=True
        customer_data.config['WTF_CSRF_ENABLED']=False
       
       
    def tearDown(self):
        pass

    def test_registration(self):
        tester=customer_data.test_client(self)
        response=tester.get('/auth/signup/',content_type='html/text')
        self.assertNotEqual(response.status_code,404)

    def test_registration_loads(self):
        tester=customer_data.test_client(self)
        response=tester.get('/auth/signup/',content_type='html/text')
        self.assertTrue(b'Username' in response.data)

    def test_registration_correct_credentials(self,username,email,password,confirm_password,follow):
        tester=customer_data.test_client(self)
        return tester.post('/auth/signup/',
            data=dict(username=username,
            email=email,
            password=password,
            confirm_password=confirm_password),
            follow_redirects=follow
            )
    def test_registration_incomplete(self):
        response=self.test_registration_correct_credentials('','','','',False)
        self.assertIn(b"This field is required",response.data)
    
    def test_registration_pass_notlong(self):
        response=self.test_registration_correct_credentials('','','856','856',False)
        self.assertIn(b"Field must be between 8 and 16 characters long.",response.data)
    
    def test_pass_notEqual_cpass(self):
        response=self.test_registration_correct_credentials('','','password','passworw',False)
        self.assertIn(b"Field must be equal to password.",response.data)
    
    def test_invalid_email(self):
        response=self.test_registration_correct_credentials('','hwlodfh','password','password',False)
        self.assertIn(b"enter a valid email",response.data)
        
    def test_double_registration(self):
        response=self.test_registration_correct_credentials('DenHen112','herkn@g.com','password','password',True)
        
        self.assertIn(b"user name or email is already taken. choose another name.",response.data)
    
    def test_success_registration(self):
        response=self.test_registration_correct_credentials('DenHen12','hekn@g.com','password','password',True)
        self.assertEqual(response.status_code,302)





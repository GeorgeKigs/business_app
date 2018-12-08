from customer_data import customer_data,db,bcrypt
import unittest
from customer_data.database import Users,Companies
import random 
import string

def random_char():
       return ''.join(random.choice(string.ascii_letters) for x in range(6))

name=random_char()
email=str(name+'@gmail.com')

value=random.randint(1000000000,100000000000)


class Login_route_test(unittest.TestCase):
    def setUp(self):
        customer_data.config['TESTING']=True
        customer_data.config['WTF_CSRF_ENABLED']=False
       


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
        response=self.test_login_correct_credentials(email,'pass7word',False)
        self.assertIn(b"enter the right credentials",response.data)

    def test_no_details(self):
        response=self.test_login_correct_credentials('','',False)
        self.assertIn(b"This field is required",response.data)
        

    def test_valid_user(self):
        response=self.test_login_correct_credentials(email,'password',True)
        self.assertEqual(response.status_code,200)
   






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
        login=Login_route_test()
        login.test_login_correct_credentials(email,'password',False)
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
        self.test_success_registration()
        response=self.test_registration_correct_credentials(name,email,'password','password',True)
        
        self.assertIn(b"user name or email is already taken. choose another name.",response.data)
    
    def test_success_registration(self):
        
        response=self.test_registration_correct_credentials(name,email,'password','password',True)
        self.assertEqual(response.status_code,200)
        




# class Review_routes(unittest.TestCase):
#     def setUp(self):
#         customer_data.config['TESTING']=True
#         customer_data.config['WTF_CSRF_ENABLED']=False

#     def tearDown(self):
#         pass

#     def test_review(self):
#         tester=customer_data.test_client(self)
#         response=tester.get('/business/review/',content_type='html/text')
#         # self.assertEqual(response.status_code,200)
#         self.assertTrue(b'Name' in response.data)
   
   

#     def test_review_correct_credentials(self,name,companyname,review,follow):
#         tester=customer_data.test_client(self)
#         return tester.post('/business/reviews/',
#             data=dict(client=name,
#             companyname=companyname,
#             content=review),
#             follow_redirects=follow
#             )
#     def test_review_incomplete(self):
#         response=self.test_review_correct_credentials('','','',False)
#         self.assertIn(b"This field is required",response.data)

#     def test_no_company(self):
#         response=self.test_review_correct_credentials('gehe','grbyr','great',False)
#         self.assertIn(b"grbyr does not exsist",response.data)

#     def test_success_registration(self):
#         response=self.test_review_correct_credentials(name,email,'password',True)
#         self.assertEqual(response.status_code,302)




class Company_registration(unittest.TestCase):
    def setUp(self):
        customer_data.config['TESTING']=True
        customer_data.config['WTF_CSRF_ENABLED']=False
       
    def tearDown(self):
        pass

    def test_review_loads(self):
        tester=customer_data.test_client(self)
        response=tester.get('/business/companyreg/',content_type='html/text')
        self.assertTrue(b'Company Name' in response.data)
        # self.assertEqual(response.status_code,200)
    
    def test_companies_correct_credentials(self,name,email,valueno,
            value,companyltn,companyproduct,follow):
        tester=customer_data.test_client(self)
        login=Login_route_test()
        login.test_login_correct_credentials(email,'password',True)
        return tester.post('/business/companyreg/',
            data=dict(companyname=name,
            companydomain=email,
            companycode=valueno,
            companyno=value,
            companyltn=companyltn,
            companyproduct=companyproduct),
            follow_redirects=follow
            )
    def test_incomplete(self):
        response=self.test_companies_correct_credentials('','','','','','',True)
        self.assertIn(b"This field is required",response.data)
    def test_double_companies(self):
        self.test_success()
        response=self.test_companies_correct_credentials(name,email,
            value,value,value,'kuku',False)
        self.assertIn(b"user name or email is already taken. choose another name.",response.data)
    def test_invalid_domain(self):
        response=self.test_companies_correct_credentials('','heywt','','','','',True)
        self.assertIn(b"Invalid email address",response.data)    
    
    
    def test_success(self):
        
        response=self.test_companies_correct_credentials(name,email,value,
            value,'Ruiru','kuku',True)
        self.assertEqual(response.status_code,302)
        return value



if __name__ == "__main__":
    unittest.main()
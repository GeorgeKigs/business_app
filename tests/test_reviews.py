from customer_data import customer_data,db,bcrypt
import unittest
from customer_data.database import Users,Companies
from random import randint

class Review_routes(unittest.TestCase):
    def setUp(self):
        customer_data.config['TESTING']=True
        customer_data.config['WTF_CSRF_ENABLED']=False

    def tearDown(self):
        pass

    def test_review(self):
        tester=customer_data.test_client(self)
        response=tester.get('/business/review/',content_type='html/text')
        # self.assertEqual(response.status_code,200)
        self.assertTrue(b'Name' in response.data)
   
   

    def test_review_correct_credentials(self,name,companyname,review,follow):
        tester=customer_data.test_client(self)
        return tester.post('/business/reviews/',
            data=dict(client=name,
            companyname=companyname,
            content=review),
            follow_redirects=follow
            )
    def test_review_incomplete(self):
        response=self.test_review_correct_credentials('','','',False)
        self.assertIn(b"This field is required",response.data)

    def test_no_company(self):
        response=self.test_review_correct_credentials('gehe','grbyr','great',False)
        self.assertIn(b"grbyr does not exsist",response.data)

    def test_success_registration(self):
        response=self.test_review_correct_credentials('DenHen','hello','password',True)
        self.assertEqual(response.status_code,302)

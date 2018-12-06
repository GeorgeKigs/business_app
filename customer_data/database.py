from customer_data import db
import datetime

'''connect to the PostgreSql database server'''

class Users(db.Model):
    ''' class to input the users in the database from the 
    reistration form'''
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(30),unique=True,nullable=False)
    password=db.Column(db.String(),nullable=False)
    code=db.relationship('Companies',backref='user',lazy=True)
    

class Companies(db.Model):
    ''' class to import the registered companies into the database from
    the company registration form
    '''
    
    id = db.Column(db.Integer,primary_key=True)
    companyname=db.Column(db.String(20),unique=True,nullable=False)
    companydomain=db.Column(db.String(30),unique=True,nullable=False)
    companycode=db.Column(db.String(40),unique=True,nullable=False)
    companyltn=db.Column(db.String(20),nullable=False)
    companyno=db.Column(db.String(12),unique=True,nullable=False)
    companyproduct=db.Column(db.String(100),unique=False,nullable=False,default='to be updated')
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),
    nullable=False)

class Reviews_db(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    time=db.Column(db.DateTime, default=datetime.datetime.utcnow)
    companyname=db.Column(db.String(20),nullable=False)
    companyid=db.Column(db.String(40),nullable=False)
    user_id=db.Column(db.Integer,nullable=False)
    content=db.Column(db.String(),nullable=False)




    
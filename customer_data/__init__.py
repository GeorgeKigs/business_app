from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


customer_data=Flask(__name__)

customer_data.config['SECRET_KEY']="thisis623ots1025ple7se8564"

##to connect to the postgres database
customer_data.config['SQLALCHEMY_DATABASE_URI']='''postgresql://george:password@localhost/customer'''

db = SQLAlchemy(customer_data)
bcrypt=Bcrypt(customer_data)

from customer_data import routes
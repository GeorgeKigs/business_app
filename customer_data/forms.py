from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class RegistrationForm(FlaskForm):
    username=StringField("Username",
            validators=[DataRequired(),Length(min=3,max=16)])
    email=StringField("Email",
            validators=[DataRequired(),Email("enter a valid email")])
    password=PasswordField("Password",
            validators=[DataRequired(),Length(min=8,max=16)])
    confirm_password=PasswordField("Confirm Password",
            validators=[DataRequired(),Length(min=8,max=16),EqualTo('password')])
    submit=SubmitField("Sign Up")



class LoginForm(FlaskForm):

    email=StringField("Email",
        validators=[DataRequired(),Email()])
    password=PasswordField("Password",
            validators=[DataRequired(),Length(min=8,max=16)])
    remenber=BooleanField("remember me")
    submit=SubmitField("Log In")

class CompanyRegistration(FlaskForm):
        companyname=StringField("Company Name: ",validators=[DataRequired()])
        companydomain=StringField("Comapany Domain: ",
                validators=[DataRequired(),Email()])
        companycode=StringField("KRA Code: ",
                validators=[DataRequired()])
        companyno=StringField("Telephone No: ",
                validators=[DataRequired(), Length(min=10, max=12)])
        companyltn=StringField("Location",
                validators=[DataRequired(),Length(min=5)])
        companyproduct=StringField("Product",validators=[DataRequired()])
        submit=SubmitField("Register")

class Delete_com(FlaskForm):
        companycode=StringField("KRA Code: ",
                validators=[DataRequired()])
        password=PasswordField("Password",
            validators=[DataRequired(),Length(min=8,max=16)])
        submit=SubmitField("Delete")
class Reviews(FlaskForm):
        client=StringField("Name:", 
        validators=[DataRequired(),Length(max=20)])
        ## create a new table with relationships between the customer and his company
        companyname=StringField("Company Name: ",validators=[DataRequired()])
        content=TextAreaField('reviews',
                validators=[DataRequired()])
        submit=SubmitField('Send')
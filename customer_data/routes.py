from flask import  render_template,url_for,request,flash,redirect
from customer_data.database import Users,Companies,Reviews_db
from customer_data.forms import RegistrationForm,LoginForm,CompanyRegistration,Delete_com,Reviews
from customer_data import customer_data,db,bcrypt

success=False



@customer_data.route("/auth/login/",methods=['POST','GET'])
def login():
    global success,email_val
    form=LoginForm()
    
    if form.validate_on_submit():
        email_val=Users.query.filter_by(email=form.email.data).first()
        
       
        if email_val and bcrypt.check_password_hash(email_val.password,form.password.data):
            flash(f'account {form.email.data} is successfully created','success')
            success=True
            return redirect(url_for("business"))

        else:
            flash("enter the right credentials")
            
    return render_template('login.html',title="Log In" ,form=form)



@customer_data.route("/auth/signup/" ,methods=['POST','GET'])
def signup():
   
    register=RegistrationForm()

    if register.validate_on_submit():

        ## encrypt the password from the method imported from the forms.py
        

        ## validate whether the user name and the email is in the database
        user_vaidate=Users.query.filter_by(username=register.username.data).first()
        email_validate=Users.query.filter_by(email=register.email.data).first()
        if user_vaidate or email_validate:
            flash('user name or email is already taken. choose another name.')
            return redirect(url_for('signup'))
        hashed_password=bcrypt.generate_password_hash(register.password.data).decode('utf-8')
        user=Users(username=register.username.data,email=register.email.data,
        password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'account {register.username.data} is successfully created','success')
        return redirect(url_for("login"))
    return render_template('signup.html',title="Sign Up", form=register)

@customer_data.route("/", methods=['POST','GET'])
@customer_data.route('/business/',methods=['POST','GET'])
def business():
    name="Please Log In"
    review=Companies.query.all()
    return render_template('business.html',title='business',name=name,
        success=success,review=review)



@customer_data.route('/business/companyreg/', methods=['POST','GET'])
def companyreg():


    form=CompanyRegistration()
    if form.validate_on_submit():
        compname_vaidate=Companies.query.filter_by(companyname=form.companyname.data).first()
        compdom_validate=Companies.query.filter_by(companydomain=form.companydomain.data).first()
        compno_validate=Companies.query.filter_by(companyno=form.companyno.data).first()
        compcode_validate=Companies.query.filter_by(companydomain=form.companycode.data).first()

        if compname_vaidate or compdom_validate or compcode_validate or compno_validate:
            flash('check your details. Already taken.')
            return redirect(url_for('companyreg'))

        companydb=Companies(companyname=form.companyname.data,companydomain=form.companydomain.data,
            companycode=form.companycode.data,companyltn=form.companyltn.data,
            companyno=form.companyno.data,companyproduct=form.companyproduct.data,
            user_id=email_val.id)

        db.session.add(companydb)
        db.session.commit()
        flash('account created successfully')
        return redirect(url_for('business'))
    posts=Reviews_db.query.all

    return render_template('company.html',title='Comapny Registration',form=form,success=success,
    posts=posts)



@customer_data.route('/business/delete/', methods=['POST','GET'])
def deletecom():
    form=Delete_com()
    if form.validate_on_submit():
        code=Companies.query.filter_by(companycode=form.companycode.data).first()
        user_id=code.user_id
        id=Users.query.filter_by(id=user_id).first()
        pswd=id.password

        if code and pswd==form.password.data:
            db.session.delete(code)
            db.session.commit()
            flash(f"{form.companycode.data}account has been deleted")
            return redirect(url_for('business'))
        else:
            flash('enter the right credentials :/')
    return render_template('delete_com.html',title='Delete Company',form=form)


@customer_data.route('/business/reviews/',methods=['POST','GET'])
def reviews_form():
    form=Reviews()
    post=False
    if success:
        post=Reviews_db.query.filter_by(user_id=email_val.id)
        # if not post:
        #     flash('no posts available')
        if form.validate_on_submit():
            code=Companies.query.filter_by(companyname=form.companyname.data).first()
            
            if code:
            
                reviews_id=Reviews_db(companyname=form.companyname.data,
                    content=form.content.data,companyid=code.id,
                    user_id=code.user_id)
                db.session.add(reviews_id)
                db.session.commit()
                flash('your comment has been posted')
                return redirect(url_for('business'))
            else:
                flash(f'{form.companyname.data} does not exsist')
    
    
    return render_template('reviews.html',title='Reviews' ,form=form,post=post)


@customer_data.route('/business/<int:id>/',methods=['POST','GET'])
def post(id):
    posts=Reviews_db.query.filter_by(id=id)
    content=Companies.query.filter_by(user_id=id)
    if not posts:
        flash("no reviews posted")
        return redirect("url_for('business')")
    return render_template('post.html',title=id, post=posts,content=content)
# Arcade Database System
# description: this is a database for a arcade which hold information of everyday
# transactions, and mulitple users who need to access this database. This includes
# the administrators, employees, and members who sign up with the arcades membership
# program. Members will be able to buy time to spend in the arcade and then store
# that time whenever they checkout and the information will be stored within the
# database. Members will also be able to store SavedData of files they would like
# saved in the Database.
#
# Author: Othman Wahab
# Project: Database Project
# Class: COSC 471 Summer 2019

from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, TransactionForm
# from database import database_session
from flask_bcrypt import Bcrypt
# from flask_login import login_user


app = Flask(__name__)
app.config['SECRET_KEY'] = '423a3ab765531776d30b248ceb78b87d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    fName = db.Column(db.String(25), nullable=False)
    lName = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Administrator('{self.fName}', '{self.lName}', '{self.email}', '{self.phone}')"

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    fName = db.Column(db.String(25), nullable=False)
    lName = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Employee('{self.fName}', '{self.lName}', '{self.email}', '{self.phone}')"

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
    fName = db.Column(db.String(25), nullable=False)
    lName = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    minutes = db.Column(db.Integer, nullable=False, default=0)
    temp = db.Column(db.Boolean, nullable=False, default=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Member('{self.fName}', '{self.lName}', '{self.email}', '{self.phone}', '{self.minutes}')"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment = db.Column(db.Boolean, nullable=False, default=False)
    amount = db.Column(db.Integer, nullable=False)
    product = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False, default=0)

    def __repr__(self):
        return f"Transaction('{self.id}', '{self.date}', '{self.payment}', '{self.amount}')"

class SavedData(db.Model):
    title = db.Column(db.String(100), nullable=False, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data = db.Column(db.LargeBinary, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)

    def __repr__(self):
        return f"Transaction('{self.id}', '{self.date}', '{self.payment}', '{self.amount}')"


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content:': 'First post content',
        'date_posted': 'April 21, 2019'
    }

]


@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.type.data == 0:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            admin = Administrator(fName= form.fName.data, lName = form.lName.data, email = form.email.data, phone= form.phone.data, password=hashed_password)
            db.session.add(admin)
            db.session.commit()
            flash('Your account has been created! You are now able to login.', 'success')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            employee = Employee(fName= form.fName.data, lName = form.lName.data, email = form.email.data, phone= form.phone.data, password=hashed_password)
            db.session.add(employee)
            db.session.commit()
            flash('Your account has been created! You are now able to login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/")
@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userType = form.type.data
        user = userType.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('userType'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/admin")
def Administrator():
    # administratorArray = []
    # data = {}
    # counterAdministrator = 1
    #
    # # Build Dictionary admins
    # for administrator in database_session.query(Administrator):
    #     data['id'] = counterAdministrator
    #     currentAdministrator = administrator.id
    #     data['administrator'] = currentAdministrator
    #     administratorArray.append(data)
    #
    #     counterAdministrators += 1
    #     data = {}



    return render_template('admin_index.html', title = 'Administrator', link1=url_for('Administrator'), link2 =url_for('viewUsers') , link3=url_for('viewStatistics') , link4 =url_for('createMember') )

@app.route("/viewUsers")
def viewUsers():
    return render_template('viewUsers.html', title = 'View Users', link1=url_for('Administrator'))

@app.route("/viewStatistics")
def viewStatistics():
    return render_template('viewStatistics.html', title = 'View Statistics', link1=url_for('Administrator'))

@app.route("/createMember")
def createMember():
    form = RegistrationForm()
    if form.validate_on_submit():
        userType = form.type.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        member = userType(fName= form.fName.data, lName = form.lName.data, email = form.email.data, phone= form.phone.data, password=hashed_password)
        db.session.add(member)
        db.session.commit()
        flash('You have successfully created a new Member.', 'success')
        return redirect(url_for('createMember'))

    return render_template('create_member.html', title = 'Create Member', link1=url_for('login'), form = form)

@app.route("/employee")
def Employee():
    return render_template('employee_index.html', title = 'Employee', link1=url_for('Employee'), link2=url_for('transaction'), link3=url_for('modify'), link4=url_for('viewMembers'), link5=url_for('createMember'))

@app.route("/transaction")
def transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        cart = Transaction(product = form.product.data, amount = form.amount.data, id = form.id.data, payment = form.payment.data)
        db.session.add(cart)
        db.session.commit()
        flash('You have successfully completed a transaction.', 'success')
        return redirect(url_for('transaction'))
    return render_template('transaction.html', title = 'Transaction', link1=url_for('Employee'),form = form)

@app.route("/modify")
def modify():
    form = RegistrationForm()
    if form.validate_on_submit():
        userType = form.type.data
        member = userType(fName= form.fName.data, lName = form.lName.data, email = form.email.data, phone= form.phone.data)
        db.session.query(member)

    return render_template('modify.html', title = 'Modify Members', link1=url_for('Employee'), form = form)

@app.route("/viewMembers")
def viewMembers():
    return render_template('viewMembers.html', title = 'View Members', link1=url_for('Employee'))

@app.route("/member")
def Member():
    return render_template('member.html', title = 'Member', link1=url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

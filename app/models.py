from hashlib import md5
from datetime import datetime, date
from datetime import date, timedelta
import dateutil.relativedelta
import dateutil.parser
import dateutil.rrule
import calendar
import string
import random
from faker import Faker
import csv
from decimal import Decimal
import csv
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask_login import UserMixin
from app import db, login
from sqlalchemy.orm import sessionmaker
import emoji

# Set up user_loader
@login.user_loader
def load_user(user_id):
    #return Employee.query.get(int(user_id))
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', \
        '{self.image_file}','{self.date_created}', '{self.is_admin}')"

    
    @property
    def password(self):

        raise AttributeError('password is not a readable attribute.')
    
    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    phone_number=db.Column(db.String(16), index=True)
    gender = db.Column(db.String(60), index=True)
    address=db.Column(db.String(120), index=True)
    city = db.Column(db.String(30), index=True)
    state = db.Column(db.String(20), index=True) 
    country = db.Column(db.String(20), index=True)   
    birthday = db.Column(db.DateTime)
    date_of_employment = db.Column(db.DateTime)
    passport_pic = db.Column(db.String(50), default='default.png')
    employee_id = db.Column(db.String(16), index=True)
    # Here we define the relationship
    lap_id = db.Column(db.Integer, db.ForeignKey('laps.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    
    is_notified = db.Column(db.Boolean, default=False)
    expat_id = db.Column(db.String(16), index=True)
    # Here we define further 
    emergencies = db.relationship('Emergency', backref='employee', lazy='dynamic')
    passports = db.relationship('Passport', backref='employee', lazy='dynamic')
    cerpacs = db.relationship('Cerpac', backref='employee', lazy='dynamic')
    #We set properties for actual age from Birthday
    get_age = db.Column(db.DateTime)
    get_bday = db.Column(db.DateTime)
    employment_age =  db.Column(db.DateTime)

    def __repr__(self):
           return '<Employee {}>'.format(self)

    @property
    def get_age(self):

        today = date.today()
        try:
            birthday = (self.birthday).replace(year = today.year)

    # raised when birth date is February 29 
    # and the current year is not a leap year 
        except ValueError:
            birthday = (self.birthday).replace(year = today.year, 
                    month = (self.birthday).month + 1, day = 1) 
            #print(birthday)
        if birthday.date()  > today:
            age =  today.year -(self.birthday).year - 1
            return (age)

        else: 
            age = today.year - (self.birthday).year
            return (age) 

    
    @property
    def get_bday(self):

        today = datetime.now()
        #time =  self.expired_date - datetime.now()
        bday = (self.birthday).replace(year = today.year) 
        #print(bday)
        #bday = date(today.year,6,30)
        diff = (bday - today).days
        diffu = diff+1
        flag = "check later"
        if diffu < 0 :
            bdays = (self.birthday).replace(year = today.year + 1) 
            flag =  bdays.strftime('%d,%B, %Y')
            #lag = " check %d " %diffu 
        elif diffu ==0 and diffu <1:
            flag = (emoji.emojize("#Bday Hurray! :birthday_cake:",variant="emoji_type"))
      

        elif diffu ==1:
                flag = (emoji.emojize("#Bday Tomorrow! :thumbs_up:",variant="emoji_type"))

        elif diffu >1 and diffu < 8:
            flag =  ( "# {}".format(diffu) + " Days Left! " + " \U0001F389 " )

        elif diffu >8 and diffu <=30:
            flag= ("# {}" .format(diffu) + " Days Left " + "\U0001F44C " )
          
        else:
            flag = bday.strftime('%d,%b, %Y')   
        return (flag)
            
    @property    
    def renew_status(self):

        flag = 'Active'
        if self.remaining_days <= 410  and self.remaining_days > 365:
                flag = 'warning'
        elif self.remaining_days <=365 :
                flag = 'Expired'
        return(flag)

  


class Department(db.Model):
        __tablename__ = 'departments'
        id = db.Column(db.Integer, primary_key=True) 
        name = db.Column(db.String(60), unique=True)
        description = db.Column(db.String(200))
        expat_id = db.Column(db.String(16), index=True)
        employees = db.relationship('Employee', backref='department', lazy='dynamic')
        

        def __init__(self, name, description):
            self.name = name
            self.description = description


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    expat_id = db.Column(db.String(16), index=True)
    employees = db.relationship('Employee', backref='role', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Emergency(db.Model):
        __tablename__ = 'emergencies'
        id = db.Column(db.Integer, primary_key=True) 
        name = db.Column(db.String(60), unique=True)
        phone = db.Column(db.String(16), index=True)
        relationship = db.Column(db.String(16), index=True)
        address = db.Column(db.String(200))
        expat_id = db.Column(db.String(16), index=True)
        employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
        
        def __repr__(self):
            return '<Emergenncy {}>'.format(self.name)






class Cerpac(db.Model):
        __tablename__ = 'cerpacs'
        id = db.Column(db.Integer, primary_key=True) 
        cerpac_issue_date = db.Column(db.DateTime)
        expired_date = db.Column(db.DateTime)
        remaining_days = db.Column(db.DateTime)
        cerpac_serial_no = db.Column(db.String(60))
        cerpac_upload = db.Column(db.String(20), default='cerpac.jpg')
        renew_status = db.Column(db.Boolean)
        process_status = db.Column(db.Boolean, default=False)
        expat_id = db.Column(db.String(16), index=True)
        renewcerpac_id = db.Column(db.Integer, db.ForeignKey('renewcerpacs.id'))
        renews = db.relationship('Renew', backref='cerpac',lazy='dynamic')
        employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
                
        def __repr__(self):
             return '<Cerpac {}>'.format(self)
    
        @property
        def remaining_days(self):
            time =  self.expired_date - datetime.now()
            #print(self.expired_date)
            #print(self.cerpac_issue_date)
            #return (time).days
            return (time).days
            
        @property    
        def renew_status(self):
            flag = 'Active'
            if self.remaining_days <= 410  and self.remaining_days > 365:
                    flag = 'warning'
            elif self.remaining_days <=365 :
                    flag = 'Expired'
            return(flag)

        @property
        def days_to_expiry(self):
            return (self.cerpac_exp_date - datetime.now()).days


class Company(db.Model):
        __tablename__ = 'companies'
        id = db.Column(db.Integer, primary_key=True) 
        company_name= db.Column(db.String(60), unique=True)
        company_address = db.Column(db.String(200))
        company_email = db.Column(db.String(120), index=True, unique=True)
        contact_number = db.Column(db.String(120), index=True, unique=True)
        nature=  db.Column(db.String(120), index=True, unique=True)
        logo_image = db.Column(db.String(30), default='default.png')
        expat_id = db.Column(db.String(16), index=True)
        quota = db.relationship('Quota', backref='company',lazy='dynamic')
        employee = db.relationship('Employee', backref='company', lazy='dynamic')
        
        

        def __repr__(self):
            return '<Company {}>'.format(self)
       

class Quota(db.Model):
        __tablename__ = 'quotas'
        id = db.Column(db.Integer, primary_key=True)
        no_of_positions = db.Column(db.Integer)
        effective_date =db.Column(db.DateTime)
        quota_exp_date = db.Column(db.DateTime)
        quota_upload = db.Column(db.String(30),  default='quota.jpg')
        quota_reference = db.Column(db.String(60), unique=True)
        remaining_days = db.Column(db.DateTime)
        renew_status = db.Column(db.Boolean, default=False)
        process_status = db.Column(db.Boolean, default=False)
        expat_id = db.Column(db.String(16), index=True)
        renewquota = db.relationship('Renewquota', backref='quota',lazy='dynamic')
        renews = db.relationship('Renew', backref='quota',lazy='dynamic')
        # here we define a relationship
        company_id =  db.Column(db.Integer, db.ForeignKey('companies.id'))
        lap_id = db.Column(db.Integer, db.ForeignKey('laps.id'))
        token_serial_id = db.Column(db.Integer, db.ForeignKey('token_serials.id'))
        
        def __repr__(self):
            return '<Quota {}>'.format(self)

        @property
        def remaining_days(self):
            time =  self.quota_exp_date - datetime.now()
            #print(self.quota_exp_date)
            #print(self.effective_date)
            return (time).days
            
        @property    
        def renew_status(self):
            flag = 'Active'
            if self.remaining_days <= 410  and self.remaining_days > 365:
                    flag = 'warning'
            elif self.remaining_days <=365 :
                    flag = 'Expired'
            return(flag)


class Passport(db.Model):
        __tablename__ = 'passports'
        id = db.Column(db.Integer, primary_key=True) 
        nationality = db.Column(db.String(60))
        passport_no = db.Column(db.String(16), unique=True)
        renew_status = db.Column(db.Boolean, default=False)
        process_status = db.Column(db.Boolean, default=False)
        remaining_days = db.Column(db.DateTime)
        passport_exp_date = db.Column(db.DateTime)
        passport_issue_date = db.Column(db.DateTime)
        count_down = db.Column(db.DateTime)
        expat_id = db.Column(db.String(16), index=True)
        renewpassport_id = db.Column(db.Integer, db.ForeignKey('renewpassport.id'))
        renews = db.relationship('Renew', backref='passport',lazy='dynamic')
        employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
        def __repr__(self):
            return '<Passport {}>'.format(self)
        
        @property
        def remaining_days(self):
            #time =  self.passport_exp_date - self.passport_issue_date
            time = self.passport_exp_date - datetime.now()
            #print(self.passport_exp_date)
            #print(self.passport_issue_date)
            #print(datetime.date.today())
            return (time).days
            
        @property    
        def renew_status(self):
            flag = 'Active'
            if self.remaining_days <= 410  and self.remaining_days > 365:
                    flag = 'warning'
            elif self.remaining_days <=365 :
                    flag = 'Expired'
            return(flag)

        @property
        def count_down(self):
            cont = self.passport_exp_date - datetime.date.today()
            print(cont)
            return(cont).days


class Renewpassport(db.Model):
        __tablename__ = 'renewpassport'
        id = db.Column(db.Integer, primary_key=True) 
        passport_issue_date = db.Column(db.DateTime)
        passport_exp_date = db.Column(db.DateTime)
        expat_id = db.Column(db.String(16), index=True)
        is_passport_renewed = db.Column(db.Boolean, default=False)
        passport = db.relationship('Passport', backref='renewpassport',lazy='dynamic')
        
        def __init__(self, passport_issue_date,passport_exp_date, 
        is_passport_renewed, passport  ):
            self.passport_issue_date = passport_issue_date
            self.passport_exp_date = passport_exp_date
            self.is_passport_renewed = is_passport_renewed
            self.passport = passport
    

class Renewquota(db.Model):
        __tablename__ = 'renewquota'
        id = db.Column(db.Integer, primary_key=True) 
        quota_issue_date = db.Column(db.DateTime)
        quota_exp_date = db.Column(db.DateTime)
        quota_reference = db.Column(db.String(60))
        expat_id = db.Column(db.String(16), index=True)
        quota_id =  db.Column(db.Integer, db.ForeignKey('quotas.id'))

        def __init__(self, quota_issue_date,quota_exp_date, quota_reference):
            self.quota_issue_date = quota_issue_date
            self.quota_exp_date = quota_exp_date
            self.quota_reference = quota_reference


class Renewcerpac(db.Model):
        __tablename__ = 'renewcerpacs'
        id = db.Column(db.Integer, primary_key=True) 
        cerpac_issue_date= db.Column(db.DateTime)
        cerpac_exp_date = db.Column(db.DateTime)
        cerpac_reference = db.Column(db.String(60))
        expat_id = db.Column(db.String(16), index=True)
        cerpac = db.relationship('Cerpac', backref='renewcerpac',lazy='dynamic')
       
        def __init__(self, cerpac_issue_date, cerpac_exp_date, cerpac_reference, cerpac ):
            self.cerpac_issue_date = cerpac_issue_date
            self.cerpac_exp_date = cerpac_exp_date
            self.cerpac_reference = cerpac_reference
            self.cerpac = cerpac
            
""" This is a test form for child and parent database and reltionship"""
class Token_serial(db.Model):
    """Stores races."""
    __tablename__ = 'token_serials'
    id = db.Column(db.Integer, primary_key=True)
    serial_no = db.Column(db.String(60))
    quotas = db.relationship('Quota', backref='token_serial',lazy='dynamic')
    laps = db.relationship('Lap', backref='token_serial',lazy='dynamic')

    def __repr__(self):
        return '<Token_serial {}>'.format(self)


class Lap(db.Model):

    __tablename__ = 'laps'
    id = db.Column(db.Integer, primary_key=True)
    token_serial_id = db.Column(db.Integer, db.ForeignKey('token_serials.id'))
    runner_name = db.Column(db.String(100))
    expat_id = db.Column(db.String(16), index=True)
    employees = db.relationship('Employee', backref='laps',lazy='dynamic')
    quotas = db.relationship('Quota', backref='laps',lazy='dynamic')
  
    def __repr__(self):
        
        return '<Lap {}>'.format(self)


class Renew(db.Model):

    __tablename__ = 'renews' 
    id = db.Column(db.Integer, primary_key=True)
    cerpac_id = db.Column(db.Integer, db.ForeignKey('cerpacs.id'))
    quota_id = db.Column(db.Integer, db.ForeignKey('quotas.id'))
    passport_id = db.Column(db.Integer, db.ForeignKey('passports.id'))
    new_issue_date = db.Column(db.DateTime)
    new_expiry_date = db.Column(db.DateTime)
    expat_id = db.Column(db.String(16), index=True)
    approvals = db.relationship('Approval', backref='renew',lazy='dynamic')
       
    def __repr__(self):
        
        return '<Renew {}>'.format(self)

class Leave(db.Model):

    __tablename__ = 'leaves'
    id = db.Column(db.Integer, primary_key=True)
    leave_type =  db.Column(db.String(60))
    Description =  db.Column(db.String(80))
    leave_date =  db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    expat_id = db.Column(db.String(16), index=True)
    approvals = db.relationship('Approval', backref='leave',lazy='dynamic')

    def __repr__(self):
        
        return '<Leave {}>'.format(self)

class Approval(db.Model):

    __tablename__ = 'approvals'
    id = db.Column(db.Integer, primary_key=True)
    renew_id = db.Column(db.Integer, db.ForeignKey('renews.id'))
    leave_id = db.Column(db.Integer, db.ForeignKey('leaves.id'))
    is_admin = db.Column(db.Boolean, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)
       
    def __repr__(self):
        
        return '<Approval {}>'.format(self)





"""
 Below code is used to generate fake datas
RECORD_COUNT =10000
fake = Faker()


def create_csv_file():
    with open('./files/invoices.csv', 'w', newline='') as csvfile:
        fieldnames = ['first_name', 'last_name', 'email', 'product_id', 'qty',
                      'amount', 'description', 'address', 'city', 'state',
                      'country']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(RECORD_COUNT):
            writer.writerow(
                {
                    'first_name': fake.name(),
                    'last_name': fake.name(),
                    'email': fake.email(),
                    'product_id': fake.random_int(min=100, max=199),
                    'qty': fake.random_int(min=1, max=9),
                    'amount': float(Decimal(random.randrange(500, 10000))/100),
                    'description': fake.sentence(),
                    'address': fake.street_address(),
                    'city': fake.city(),
                    'state': fake.state(),
                    'country': fake.country()
                }
            )


start = time()
create_csv_file()
elapsed = time() - start
print('created csv file time: {}'.format(elapsed))

"""
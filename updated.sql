from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager



class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    phone_number=db.Column(db.String(16), index=True)
    gender = db.Column(db.String(60), index=True)
    address=db.Column(db.String(200), index=True)
    employee_id = db.Column(db.String(16), index=True)
    birthday = db.Column(db.DateTime)
    date_of_employment = db.Column(db.DateTime)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    family_id = db.Column(db.Integer, db.ForeignKey('families.id'))
    passport_id = db.Column(db.Integer, db.ForeignKey('passports.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    renew_id = db.Column(db.Integer, db.ForeignKey('renew.id'))
    is_notified = db.Column(db.Boolean, default=False)


    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
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

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
        __tablename__ = 'departments'
        id = db.Column(db.Integer, primary_key=True) 
        name = db.Column(db.String(60), unique=True)
        description = db.Column(db.String(200))
        employees = db.relationship('Employee', backref='department',lazy='dynamic')

        def __repr__(self):
                return '<Department: {}>'.format(self.name)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Family(db.Model):
        __tablename__ = 'families'
        id = db.Column(db.Integer, primary_key=True) 
        spouse_name = db.Column(db.String(60), unique=True)
        spouse_phone = db.Column(db.String(16), index=True)
        residential_address = db.Column(db.String(200))
        child_1 = db.Column(db.String(60), unique=True)
        child_1_dob  = db.Column(db.DateTime)
        child_2_dob  = db.Column(db.DateTime)
        child_3_dob  = db.Column(db.DateTime)
        child_2 = db.Column(db.String(60), unique=True)
        child_3 = db.Column(db.String(60), unique=True)
        employees = db.relationship('Employee', backref='family',lazy='dynamic')

        def __repr__(self):
            return '<Family: {}>'.format(self.username)



class Cerpac(db.Model):
        __tablename__ = 'cerpacs'
        id = db.Column(db.Integer, primary_key=True) 
        company_name = db.Column(db.String(60), unique=True)
        address = db.Column(db.String(200))
        cerpac_issue_date = db.Column(db.DateTime)
        cerpac_exp_date=db.Column(db.DateTime)
        cerpac_title = db.Column(db.String(60))
        cerpac_serial_no = db.Column(db.String(60))
        passports = db.relationship('Passport', backref='cerpac',lazy='dynamic')

        def __repr__(self):
            return '<Cerpac: {}>'.format(self.username)

class Quota(db.Model):
        __tablename__ = 'quotas'
        id = db.Column(db.Integer, primary_key=True) 
        designation = db.Column(db.String(60), unique=True)
        quota_renewal_date = db.Column(db.DateTime)
        quota_exp_date = db.Column(db.DateTime)
        quota_issue_date =db.Column(db.DateTime)
        quota_reference = db.Column(db.String(60), unique=True)
        passports = db.relationship('Passport', backref='quota',lazy='dynamic')

        def __repr__(self):
            return '<Quota: {}>'.format(self.username)

class Passport(db.Model):
        __tablename__ = 'passports'
        id = db.Column(db.Integer, primary_key=True) 
        passport_name = db.Column(db.String(60), unique=True)
        nationality = db.Column(db.String(60))
        passport_no = db.Column(db.String(16), unique=True)
        passport_renewal_date = db.Column(db.DateTime)
        passport_exp_date = db.Column(db.DateTime)
        passport_issue_date = db.Column(db.DateTime)
        cerpac_id = db.Column(db.Integer, db.ForeignKey('cerpacs.id'))
        quota_id =  db.Column(db.Integer, db.ForeignKey('quotas.id'))
        employees = db.relationship('Employee', backref='passport',lazy='dynamic')

        def __repr__(self):
            return '<Passport: {}>'.format(self.username)

class Company(db.Model):
        __tablename__ = 'companies'
        id = db.Column(db.Integer, primary_key=True) 
        company_name= db.Column(db.String(60), unique=True)
        company_address = db.Column(db.String(200))
        company_email = db.Column(db.String(120), index=True, unique=True)
        date_joined = db.Column(db.DateTime)
        employees = db.relationship('Employee', backref='company',lazy='dynamic')

        def __repr__(self):
            return '<Company: {}>'.format(self.username)

class Renew(db.Model):
        __tablename__ = 'renew'
        id = db.Column(db.Integer, primary_key=True) 
        cerpac_issue_date= db.Column(db.DateTime)
        cerpac_exp_date = db.Column(db.DateTime)
        cerpac_reference = db.Column(db.String(60))
        quota_issue_date = db.Column(db.DateTime)
        quota_exp_date = db.Column(db.DateTime)
        quota_reference = db.Column(db.String(60))
        passport_issue_date = db.Column(db.DateTime)
        passport_exp_date = db.Column(db.DateTime)
        visa_issue_date = db.Column(db.DateTime)
        visa_expiry_date = db.Column(db.DateTime)
        visa_reference = db.Column(db.String(60))
        is_quota_renewed = db.Column(db.Boolean, default=False)
        is_cerpac_renewed = db.Column(db.Boolean, default=False)
        is_cerpac_renewed = db.Column(db.Boolean, default=False)
        is_out_of_Nigeria = db.Column(db.Boolean, default=False)
        employees = db.relationship('Employee', backref='renew',lazy='dynamic')

        def __repr__(self):
            return '<Renew: {}>'.format(self.username)
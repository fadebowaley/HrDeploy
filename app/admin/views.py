from datetime import datetime, date
import dateutil.relativedelta
import dateutil.parser
import dateutil.rrule
import calendar
from flask import abort, flash, redirect, render_template, \
url_for, g, jsonify, current_app, request
from flask_login import current_user, login_required
import os
import secrets
import string
import random
from werkzeug.utils import secure_filename

#from flask_babel 
# import _, get_locale
#from guess_language import guess_language
#from app import db
#from app.translate import translate
from hashlib import md5
from PIL import Image
from app.admin import bp
from app.admin.forms import DepartmentForm, EmployeeForm, EmergencyForm, QuotaPositionForm,  \
CerpacForm, RoleForm, CompanyForm, PassportForm, QuotaForm, EmployeeAssignForm, \
    LapForm, MainForm, QuotaRenewForm

from app import db, session, sessionmaker
from app.auth.forms import RegistrationForm
from app.models import Department, Employee, Cerpac, Role, Company, Emergency,  \
 Passport, Quota, User, Token_serial, Lap, Renew, Leave


ALLOWED_EXTENSIONS = set(['png', 'pdf', 'jpg', 'jpeg', 'gif', ])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def  check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

def check_super_admin():   
    if not current_user.is_super_admin:
        abort(403)

def  set_status():
    if  current_user.is_admin:
        ceparc.renew-status == True
       

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    #g.locale = str(get_locale())



@bp.route('/users', methods=['GET', 'POST'])
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()

    return render_template('admin/users/users.html',
                           users=users, title="users")
               

@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Add a user to the database
    """
    check_admin()
    add_user = True

    form = RegistrationForm()
    if form.validate_on_submit():
        
        user = User(username=form.username.data,
            email=form.email.data,
                password=form.password.data,
                is_admin=form.is_admin.data )
        user.date_created = datetime.utcnow()        
        try:
            # add user to the database
            db.session.add(user)
            db.session.commit()
            #send_welcome_email(user)
            flash('You have successfully added a new user.')
        except:
            # in case user name already exists
            flash('Error: user name already exists.')

        # redirect to users page
        return redirect(url_for('admin.list_users'))

    # load user template
    return render_template('admin/users/user.html', action="Add",
                           add_user=add_user, form=form,
                           title="Add User")


@bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    check_admin()

    add_user = False
    user = User.query.get_or_404(id)
    form = RegistrationForm(obj=user)
    if form.validate_on_submit():
        user.is_super_admin = form.is_super_admin.data
        db.session.commit()
        flash('You have successfully edited the user.')


        # redirect to the users page
        return redirect(url_for('admin.list_users'))
    
    form.is_super_admin.data = user.is_super_admin
    return render_template('admin/users/user_edit.html', action="Edit",
                           add_user=add_user, form=form,
                           user=user, title="Edit User")


@bp.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    #check_admin() - UnboundLocalError
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')
    # redirect to the users page
    return redirect(url_for('admin.list_users'))
    return render_template(title="Delete User")



@bp.route('/users/show/<int:id>')
@login_required
def show_user(id):
    #users = User.query.all()
    user = User.query.get_or_404(id)
    if user.id == id:
            found_user = user
    return render_template('admin/users/show.html', user = found_user, show_user=show_user, title="Show User" )



# Department Views
@bp.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")
               

@bp.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()
    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@bp.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@bp.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    #check_admin() - UnboundLocalError
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')
    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))
    return render_template(title="Delete Department")



@bp.route('/departments/show/<int:id>')
@login_required
def show_department(id):
    #departments = Department.query.all()
    department = Department.query.get_or_404(id)
    if department.id == id:
            found_department = department
    return render_template('admin/departments/show.html', department = found_department, show_department=show_department, title="Show Department" )

    """ Now we want to add more Information and Update Expatriates"""


    def check_admin():
    # prevent non-admins from accessing the page
        if not current_user.is_admin:
            abort(403)


# Expatriates  Views
""" Second View for Employee list, I call it Databox"""


@bp.route('/expatriates', methods=['GET', 'POST'])
@login_required
def list_expart_view():

    #List all expatriates that works here

    check_admin()
    employees = Employee.query.all()
    #image_file = url_for('static', filename='passports/' + Employee.image_file)  
    return render_template('admin/employees/dataview.html',
                           employees=employees,  title="Employees")



@bp.route('/employees', methods=['GET', 'POST'])
@login_required
def list_employees():
    """
    List all expatriates that works here and also Passport from Directory
    """
    check_admin()
    employees = Employee.query.all()
    
       
    return render_template('admin/employees/show.html', 
                           employees=employees, title="Employees")



@bp.route('/employees/report', methods=['GET', 'POST'])
@login_required
def employees_report():
    """
    List all expatriates Details in a comprehensive manner 
    """
    check_admin()
    employees = db.session.query(Employee, Passport, Cerpac, Lap, Company).\
        select_from(Employee).join(Passport).join(Cerpac).join(Lap).join(Company).all()
           
    return render_template('admin/employees/report.html', 
                           employees=employees, title="Employees")



@bp.route('/companies/report', methods=['GET', 'POST'])
@login_required
def companies_report():
    """companies Details in a comprehensive manner 
    """
    check_admin()
    companies = db.session.query(Quota, Company, Token_serial, Lap).\
        join(Company, Token_serial, Lap).distinct(Token_serial.serial_no).all()
    
    return render_template('admin/companies/report.html', 
                           companies=companies, title="Employees")




@bp.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):

    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)
    form = EmployeeAssignForm(obj=employee)
    
    employee.department = form.department.data
    employee.role = form.role.data
    db.session.add(employee)
    db.session.commit()
    flash('You have successfully assigned a department and role.')

        # redirect to the roles page
    return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee_assign.html',
                           employee=employee, form=form,
                           title='Assign Employee')


def expat_gen():
    chars = string.digits
    serial ='EMP-ID 000' + ''.join(random.choice(chars) for _ in range(4))  
    return(serial)


@bp.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    """
    Add a an  Employee/ expartriates  to the database
    """
    check_admin()
    add_employee = True
    form = EmployeeForm()
    #if form.validate_on_submit():
    #if request.method == 'POST':
    if request.method == 'POST':

        passport_pic = request.files['passport_pic']
        if passport_pic and allowed_file(passport_pic.filename) and form.first_name.data != "" and form.email.data != "":
            filename = secure_filename(passport_pic.filename)
            passport_pic.save(os.path.join(current_app.root_path,'static/passports', filename))  
            employee = Employee(passport_pic = filename,
            email = form.email.data, 
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number = form.phone_number.data,
            gender=form.gender.data, 
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            country=form.country.data,
            birthday=form.birthday.data, 
            date_of_employment=form.date_of_employment.data, 
            employee_id = form.employee_id.data,  
            #role = form.role.data,
            laps = form.laps.data,
            company = form.company.data,
            expat_id = expat_gen()           
             )   
                 
        #try:
            # add employee to the database
            db.session.add(employee)
            db.session.commit()
            flash('You have successfully added {}, {} with New ID {}' .format( employee.last_name, employee.first_name, employee.expat_id ))

            return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/add.html', action="Add",
                           add_employee=add_employee, form=form, 
                           title="Add Employee")      
        #except:
            # in case employee name already exists
            #flash('Error: employee name already exists.')
   
        # redirect to employee list  page
            #return redirect(url_for('admin.list_employees'))
    # load expatriate template
    
    #return render_template('admin/employees/add.html', action="Add",
                           #add_employee=add_employee, form=form, 
                           #title="Add Employee")

                           


"""Show a Particular Employee"""

@bp.route('/employees/show/<int:id>')
@login_required
def show_employee(id):

    employees = Employee.query.all()

    employee = Employee.query.get_or_404(id)

    if employee.id == id:
        found_employee = employee
    #passport_pic = url_for('static', filename='passport/' + employee.passport_pic)
    return render_template('admin/employees/show_employee.html', employee= found_employee, show_employee=show_employee,   title="Show Employee" )
    #return render_template('admin/employees/uwara.html', show_employee=show_employee,   title="Show Employee" )


@bp.route('/employees/all/<int:id>')
@login_required
def show_table(id):
    success =db.session.query(
    Employee, 
    Passport, 
    Cerpac,
    Emergency
    ).filter(
    Employee.id == Cerpac.employee_id
    ).filter(
    Employee.id == Passport.employee_id
    ).filter(
    Employee.id == Emergency.employee_id
    ).filter(
    Employee.id == id
    ).all()

    return render_template('admin/employees/show_data.html', show_table=show_table, success =success, title="Show all Employee" )
    
    

""" gather the report together here """

@bp.route('/employees/data')
@login_required
def show_all_data():

    show_table(4)    
    return render_template('admin/employees/uwara.html', show_all_data=show_all_data,  title="Show all Employee" ) 
     


    #employees =Employee.query.join(Lap).join(Company).all()
    #results = db.session.query(Employee, Passport, Cerpac, Emergency).join(Passport, Cerpac, Emergency).all()
    #results = db.session.query(Employee, Passport, Cerpac, Emergency, Lap).\
        #select_from(Employee).join(Passport).join(Cerpac).join(Emergency).join(Lap).all()

    

       
"""
    employ = db.session.query(Employee.id).count()
    companies = db.session.query(Company.id).count()
    passprt = db.session.query(Passport.id).count()
    cerpac = db.session.query(Cerpac.id).count()
    quota = db.session.query(Quota.id).count()
    positions = db.session.query(Lap.id).count()
    emergency = db.session.query(Emergency).count()
    print('No of Companies: ' , companies)
    print('No of Employees: ' , companies)
    print('No of Passports: ' , companies)
    print('No of Cerpacs: ' , companies)
    print('No of Quotas: ' , companies)
    print('Emergency Contacts', emergency)  
    print('No of Positions', positions)
"""
    #select values from multiple tables
"""    emperior = db.session.query(Employee.last_name, \
     Employee.first_name, Employee.gender, Passport.nationality, \
      Cerpac.cerpac_issue_date).join(Passport).join(Cerpac).\
        filter(Passport.id <= 2).all()

    #select 4 tables data to be populated on Company tables 
    quota1 = db.session.query(Quota, Company, Token_serial, Lap).join(Company, Token_serial, Lap).filter(Company.id==1).all()
    quota2 = db.session.query(Quota, Company, Token_serial, Lap).join(Company, Token_serial, Lap).filter(Lap.id==1).all()
    quotas = db.session.query(Quota, Company, Token_serial, Lap).\
        join(Company, Token_serial, Lap).distinct(Token_serial.serial_no).all()
    post=db.session.query(Lap.id, Lap.runner_name, Token_serial.serial_no, ).join(Token_serial).all()
    #for lap in post:
        #print(lap.runner_name)
            
    #quotaz = Quota.query.join(Company, Token_serial ).filter(Company.id==1).all()
    
    #for quota, company, token_serial, lap in quotas:
        #print( company.id, company.company_name, quota.id, token_serial.serial_no,  quota.quota_exp_date )

    #for quota, company, token_serial, lap in quota1:
        #print( quota.id, quota.quota_exp_date, company.company_name, lap.runner_name )

    #for quota, company, token_serial, lap in quota2:
        #print( quota.id, quota.quota_exp_date, company.company_name, lap.runner_name )

    #for quota, company, token_serial, lap in quotas:
        #print(quota.no_of_positions, token_serial.serial_no, company.company_name, quota.quota_exp_date)

    #for employee, passport, cerpac, emergency, lap in results:
        #print(employee.id, employee.first_name, employee.last_name, passport.nationality, cerpac.cerpac_issue_date, emergency.name, lap.runner_name)

    
    for employee in employees:

        print(employee.id, employee.first_name, employee.last_name, employee.employee_id, company.company_name, lap.runner_name,  )

    #Here we define all counts and render them accordingly to all the tables
"""



    



    

@bp.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    check_admin()
    add_employee = False
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee.employee_id = form.employee_id.data
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data  
        employee.gender = form.gender.data 
        employee.address = form.address.data  
        employee.email = form.email.data
        employee.phone_number = form.phone_number.data
        employee.birthday=form.birthday.data 
        employee.date_of_employment=form.date_of_employment.data
        employee.country=form.country.data 
        employee.city=form.city.data
        employee.state=form.state.data
        #employee.role = form.role.data
        employee.laps = form.laps.data
        employee.company = form.company.data
        db.session.add(employee)
        db.session.commit()          
        flash('You have successfully edited the Employee.')
        # redirect to the departments page
        return redirect(url_for('admin.list_employees'))

    form.employee_id.data = employee.employee_id  
    form.first_name.data = employee.first_name
    form.last_name.data  = employee.last_name 
    form.gender.data  = employee.gender
    form.address.data  = employee.address
    form.email.data = employee.email  
    form.phone_number.data= employee.phone_number  
    #form.role.data = employee.role  
    form.laps.data = employee.laps  
    form.company.data = employee.company  
    form.birthday.data  = employee.birthday
    form.date_of_employment.data = employee.date_of_employment
    form.country.data= employee.country
    form.city.data = employee.city
    form.state.data = employee.state
   
    return render_template('admin/employees/edit.html', action="Edit",
                           add_employee=add_employee, form=form, 
                           employee=employee, title="Edit Employee")




@bp.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Delete an employee from the company database
    """
    check_admin()

    employee = Employee.query.get_or_404(id)
    if os.path.exists(employee.passport_pic):
        os.remove(os.path.join(current_app.root_path,'static/passports', employee.passport_pic))
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the Employee.')

    # redirect to the departments page
    return redirect(url_for('admin.list_employees'))

    return render_template(title="Delete Employee")




"""Add Emergency contact to the Database """

@bp.route('/emergencies', methods=['GET', 'POST'])
@login_required
def list_emergencies():
    """
    List all emergencies contact for each employee that works in the organisation
    """
    check_admin()

    emergencies=Emergency.query.all()

    return render_template('admin/emergencies/show.html',
                           emergencies=emergencies, title="Emergencies")

@bp.route('/emergencies/add', methods=['GET', 'POST'])
@login_required
def add_emergency():
    """
    Add a emergencies contact for each employee that works in the organisation
    """
    check_admin()
    add_emergency = True

    form =EmergencyForm()
    if form.validate_on_submit():
        emergency = Emergency(name=form.name.data,
        phone=form.phone.data, address=form.address.data, 
        relationship=form.relationship.data, employee = form.employee.data,)
        try:
            # add department to the database
            db.session.add(emergency)
            db.session.commit()
            flash('You have successfully added  Emergency Contact for {}, {} with ID {}' .format( emergency.employee.last_name, emergency.employee.first_name, emergency.employee.expat_id ))
        except:
            # in case department name already exists
            flash('Error: family name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_emergencies'))

    # load expatriate template
    return render_template('admin/emergencies/add.html', action="Add",
                           add_emergency =add_emergency , form=form,
                           title="Add Emergency")




    """ Add Cerpac into the Database """

@bp.route('/cerpacs', methods=['GET', 'POST'])
@login_required
def list_cerpacs():
    """
    List all cerpacs
    """
    check_admin()
    cerpacs=Cerpac.query.all()
    #result = Cerpac.query().filter(employee).order_by('lastname')
    #print(result)
    return render_template('admin/cerpacs/cerpacs.html',
                           cerpacs=cerpacs,  title="Cerpacs")

@bp.route('/cerpacs/add', methods=['GET', 'POST'])
@login_required
def add_cerpac():
    """
    Add a an  Cerpac/ expartriates  to the database
    """
    check_admin()
    add_cerpac = True

    form =CerpacForm()
    if form.validate_on_submit():
        cerpac = Cerpac(cerpac_serial_no=form.cerpac_serial_no.data,
        expired_date=form.expired_date.data, 
        cerpac_issue_date= form.cerpac_issue_date.data,
        employee =form.employee.data )
                     
        try:
            #add cerpac to the database
            db.session.add(cerpac)
            db.session.commit()
            flash('You have successfully added  a Cerpac for {}, {} with ID {}' .format( cerpac.employee.last_name, cerpac.employee.first_name, cerpac.employee.expat_id ))

            
            
        except:
            # in case department name already exists
            flash('Error: cerpac name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_cerpacs'))

    # load expatriate template
    return render_template('admin/cerpacs/cerpac.html', action="Add", add_cerpac=add_cerpac, 
    form=form,  title="Add Cerpac")


@bp.route('/cerpacs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_cerpac(id):
    """
    Edit an Cerpac
    """
    check_admin()

    add_cerpac = False

    cerpac = Cerpac.query.get_or_404(id)
    form = CerpacForm(obj=cerpac)
    if form.validate_on_submit():

        cerpac.cerpac_serial_no=form.cerpac_serial_no.data
        cerpac.cerpac_issue_date= form.cerpac_issue_date.data
        cerpac.expired_date=form.expired_date.data
        cerpac.employee =form.employee.data
        
        db.session.commit()
        flash('You have successfully edited the Cerpac.')

        # redirect to the cerpacs page
        return redirect(url_for('admin.list_cerpacs'))

        form.cerpac_serial_no.data=cerpac.cerpac_serial_no
        form.cerpac_issue_date.data=cerpac.cerpac_issue_date
        form.expired_date.data=cerpac.expired_date
        form.employee.data = cerpac.add_employee
    return render_template('admin/cerpacs/cerpac.html', action="Edit",
                           add_cerpac=add_cerpac, form=form,
                           cerpac=cerpac, title="Edit Cerpac")


@bp.route('/cerpacs/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_cerpac(id):
    """
    Delete an cerpac from the company database
    """
    check_admin()

    cerpac = Cerpac.query.get_or_404(id)
    db.session.delete(cerpac)
    db.session.commit()
    flash('You have successfully deleted the Cerpac.')

    # redirect to the departments page
    return redirect(url_for('admin.list_cerpacs'))

    return render_template(title="Delete Cerpac")

@bp.route('/cerpacs/show/<int:id>')
@login_required
def show_cerpac(id):
    cerpac = Cerpac.query.get_or_404(id)
    if cerpac.id == id:
            found_cerpac = cerpac
    return render_template('admin/cerpacs/show_cerpacs.html', cerpac = found_cerpac, show_cerpac=show_cerpac, title="Show Cerpac" )


""" This Code Import Roles into the Database"""

@bp.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@bp.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@bp.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@bp.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")



@bp.route('/companies', methods=['GET', 'POST'])
@login_required
def list_companies():
    #List all companies that are affiliated here
    check_admin()
    companies=Company.query.all()
    
    return render_template('admin/companies/show.html',  companies=companies,  title="Companies")




@bp.route('/companies/add', methods=['GET', 'POST'])
@login_required
def add_company():
    #global companyAdd a an  company  to the database
    check_admin()
    add_company = True
    form = CompanyForm()
    if form.validate_on_submit():           
        if request.method == 'POST':       
            company = Company(
            company_address=form.company_address.data,
            company_name=form.company_name.data,
            company_email=form.company_email.data, 
            contact_number=form.contact_number.data )
            logo_image = request.files['logo_image']
            if logo_image and request.form.get('logo_image') !="":
                #if logo_image and allowed_file(logo_image.filename) and form.company_name.data != "" and form.company_email.data != "":
                filename = secure_filename(logo_image.filename)
                logo_image.save(os.path.join(current_app.root_path,'static/logos', filename))
                company.logo_image=filename                         
            try:        
                db.session.add(company)
                db.session.commit()
                flash('You have successfully added {}' .format(company.company_name) )
            except:
            
                flash('Error: company name already exists.')

        
        return redirect(url_for('admin.list_companies'))

    # load expatriate template
    return render_template('admin/companies/add.html', action="Add",
                           add_company=add_company, form=form,
                           title="Add Company")


@bp.route('/companies/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_company(id):
    """
    Edit an company
    """
    check_admin()

    add_company = False

    company = Company.query.get_or_404(id)
    form = CompanyForm(obj=company)
    if form.validate_on_submit():           
        
        company.company_name=form.company_name.data
        company.company_address=form.company_address.data 
        company.company_email=form.company_email.data
        company.contact_number=form.contact_number.data
        if request.method == 'POST':
            
                db.session.commit()
                flash('You have successfully edited {}' .format(company.company_name))
        
        return redirect(url_for('admin.list_companies'))
        form.company_name.data = company.company_name
        form.company_address.data = company.company_address
        form.company_email.data = company.company_email
        form.contact_number.data = company.contact_number

    return render_template('admin/companies/edit.html', action="Edit",
                           add_company=add_company, form=form,
                           company=company, title="Edit Company")


@bp.route('/companies/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_company(id):
    """
    Delete an company from the company database
    """
    check_admin()

    company = Company.query.get_or_404(id)
    image_path = os.path.join(current_app.root_path,'static/logos', company.logo_image)
    if os.path.exists(image_path):
        print('Image path located and found')
        os.remove(image_path)
    db.session.delete(company)
    db.session.commit()
    flash('You have successfully deleted {}' .format(company.company_name))

    # redirect to the departments page
    return redirect(url_for('admin.list_companies'))

    return render_template(title="Delete company")


@bp.route('/display/<filename>')
def display_image(filename):
    #if filename == Company.logo_image
	#print('display_image filename: ' + filename)
	return send_from_directory('static/logos', filename=filename)
    #return redirect(url_for('static', filename='uploads/' + filename), code=301)
    #return redirect(url_for(os.path.join(current_app.root_path,'static/logos', company.logo_image)))
    #return send_from_directory(os.path.join(current_app.root_path,'static/logos', filename))

""" Below view add Passport into the Database """

@bp.route('/passports', methods=['GET', 'POST'])
@login_required
def list_passports():
    """
    List all passports that are affiliated here
    """
    check_admin()

    passports = Passport.query.all()
    return render_template('admin/passports/passports.html',
                           passports=passports, title="Passports")


@bp.route('/passports/add', methods=['GET', 'POST'])
@login_required
def add_passport():
    
    """
    Add a pasport  to the database
    """
    check_admin()
    add_passport = True

    form = PassportForm()
    if form.validate_on_submit():
        passport = Passport(nationality=form.nationality.data,
        passport_no=form.passport_no.data,
        passport_exp_date=form.passport_exp_date.data,
        passport_issue_date=form.passport_issue_date.data,
        employee=form.employee.data)
       
        try:
            # add passport to the database
            db.session.add(passport)
            db.session.commit()
            flash('You have successfully added  a Cerpac for {}, {} with ID {}' .format( passport.employee.last_name, passport.employee.first_name, passport.employee.expat_id ))
        except:
            # in case pasport name already exists
            flash('Error: passport name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_passports'))

    # load expatriate template
    return render_template('admin/passports/passport.html', action="Add",
                           add_passport=add_passport, form=form,
                           title="Add Passport")


@bp.route('/passports/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_passport(id):
    """
    Edit a Passport
    """
    check_admin()
    add_passport = False

    passport = Passport.query.get_or_404(id)
    form = PassportForm(obj=passport)
    if form.validate_on_submit():

        passport.employee=form.employee.data
        passport.nationality=form.nationality.data
        passport.passport_no=form.passport_no.data 
        passport.passport_exp_date=form.passport_exp_date.data
        passport.passport_issue_date=form.passport_issue_date.data

        db.session.commit()
        flash('You have successfully edited the Passport.')

        # redirect to the departments page
        return redirect(url_for('admin.list_passports'))

        form.employee.data = passport.employee
        form.nationality.data = passport.nationality
        form.passport_no.data = passport.passport_no
        form.passport_exp_date.data = passport.passport_exp_date
        form.passport_issue_date.data = passport.passport_issue_date

    return render_template('admin/passports/passport.html', action="Edit",
                           add_passport=add_passport, form=form,
                           passport=passport, title="Edit Passport")


@bp.route('/passports/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_passport(id):
    """
    Delete a passport from the company database
    """
    check_admin()

    passport = Passport.query.get_or_404(id)
    db.session.delete(passport)
    db.session.commit()
    flash('You have successfully deleted the pssport.')

    # redirect to the departments page
    return redirect(url_for('admin.list_passports'))

    return render_template(title="Delete passport")


@bp.route('/quotas', methods=['GET', 'POST'])
@login_required
def list_quotas():
    """
    List all quotas here
    """
    check_admin()

    quotas=Quota.query.all()
    return render_template('admin/quotas/quotas.html',
                           quotas=quotas, title="Quotas")

  
@bp.route('/quotas/add', methods=['GET', 'POST'])
@login_required
def add_quota():

    check_admin()

    add_quota = True
    form = QuotaForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        quota_upload = request.files['quota_upload']
        if quota_upload and allowed_file(quota_upload.filename):
            filename = secure_filename(quota_upload.filename)
            quota_upload.save(os.path.join(current_app.root_path,'static/quotas', filename))

            quota = Quota(quota_upload=filename,  effective_date = form.effective_date.data,   quota_exp_date= form.quota_exp_date.data, no_of_positions = form.no_of_positions.data, quota_reference= form.quota_reference.data,
            company = form.company.data,
            token_serial= form.token_serial.data,)
        try:
            db.session.add(quota)
            db.session.commit()       
            flash('You have successfully added a quota.')
        except:         
            flash('Error: quota name already exists.')

        return redirect(url_for('admin.list_quotas'))

  
    return render_template('admin/quotas/quota.html', action="Add",
                           add_company=add_company, form=form, QuotaForm=QuotaForm,
                           title="Add Quota")


@bp.route('/quotas/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_quota(id):
    """
    Edit a Quota
    """
    check_admin()

    add_quota = False
    #company =Company.query.filter(company.id).first()
    quota = Quota.query.get_or_404(id)
    form = QuotaForm(obj=quota)
   
    if form.validate_on_submit():
        quota.no_of_positions = form.no_of_positions.data,
        quota.effective_date = form.effective_date.data
        quota.quota_exp_date=form.quota_exp_date.data
        quota.quota_reference= form.quota_reference.data
        quota.company = form.company.data
        quota.token_serial = form.token_serial.data
        db.session.add(quota)
        db.session.commit()
        flash('You have successfully edited the quota.')

        # redirect to the Quotas  page
        return redirect(url_for('admin.list_quotas'))

        form.no_of_positions.data = quota.No_of_positions
        form.effective_date.data = quota.effective_date
        form.quota_exp_date.data = quota.quota_exp_date
        form.quota_reference.data = quota.quota_reference 
        form.company.data = quota.company

    return render_template('admin/quotas/quota.html', action="Edit",
                           add_quota=add_quota, form=form,
                           quota=quota, title="Edit Quota")


@bp.route('/quotas/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_quota(id):
    """
    Delete a quota from the company database
    """
    check_admin()

    quota = Quota.query.get_or_404(id)
    db.session.delete(quota)
    db.session.commit()
    flash('You have successfully deleted the quota.')

    # redirect to the departments page
    return redirect(url_for('admin.list_quotas'))
    return render_template(title="Delete quota")


@bp.route('/quotas/show/<int:id>')
@login_required
def show_quota(id):
    quota = Quota.query.get_or_404(id)
    if quota.id == id:
            found_quota = quota
    return render_template('admin/quotas/show_quotas.html', quota = found_quota, show_quota=show_quota, title="Show Quota" )


""" This route helps us determine what we are doing dynamically"""

def serial_num():
        size=9
        chars=string.ascii_uppercase + string.digits
        serial =  ''.join(random.choice(chars) for _ in range(size))  
        return(serial)


@bp.route('/qposition', methods=['GET', 'POST'])
def add_quota_position():
    form = MainForm()
    if form.validate_on_submit():
        new_token = Token_serial(serial_no = serial_num())

        db.session.add(new_token)
        for lap in form.laps.data:
            new_lap = Lap(**lap)
             #Add to race
            new_token.laps.append(new_lap)
        db.session.commit()
    token_serials = Token_serial.query

    return render_template(
        'admin/quotapositions/razor.html',
        form=form,
       token_serials=token_serials
    )


@bp.route('/qpositions/<token_serial_id>', methods=['GET'])
def show_quota_position(token_serial_id):
    """Show the details of a race."""
    token_serial = Token_serial.query.filter_by(id=token_serial_id).first()
    #race = Race.query.filter_by(id=race_id).all()
    return render_template(
        'admin/quotapositions/show.html',
        token_serial=token_serial
    )

@bp.route('/qpositions/delete/<token_serial_id>', methods=['GET', 'POST'])
@login_required
def delete_quota_position(token_serial_id):
    """
    Delete a race from the company database
    """
    check_admin()
    token_serial = Token_serial.query.get_or_404(token_serial_id)
    db.session.delete(token_serial)
    db.session.commit()
    flash('You have successfully deleted the Quota Positions.')
    # redirect to the departments page
    return redirect(url_for('admin.add_quota_position'))
    return render_template(title="Delete Quota Positions")


@bp.route('/qpositions_all', methods=['GET', 'POST'])
@login_required
def list_all_quota_positions():
    """  List all possitions that are affiliated here  """
    check_admin()
    def get_all_position(token_serial_id=1):
        print('show all position')
    position_by = Token_serial.query.filter_by(token_serial=token_serial_id).all()
    for token_serial in token_serials:
        print(get_all_position)



""" Here we define  all renewals logic for all the form and also approval """

@bp.route('/quotas/renew/<int:id>', methods=['GET', 'POST'])
@login_required
def renew_quota(id):
    """
    renew a Quota
    """
    check_admin()

    add_quota = False
    #form = QuotaRenewForm()
    quota = Quota.query.get_or_404(id)
    form = QuotaRenewForm(obj=quota)
    if form.validate_on_submit():

        #quota.effective_date = new_issue_date.data
        #quota.quota_exp_date= new_expiry_date.data
        for renew in renew.form.data:
            new_issue_date =new_issue_date.data
            new_expiry_date = new_expiry_date.date
        db.session.add(renew)
        db.session.commit()
        flash('You have successfully renew a quota.')

        # redirect to the Quotas  page
        return redirect(url_for('admin.list_quotas'))

        form.new_issue_date.data = quota.effective_date
        form.new_expiry_date.data = quota.quota_exp_date
        form.new_expiry_date.data = renew.new_expiry_date 
        form.new_issue_date.data = renew.new_issue_date

    return render_template('admin/quotas/renew.html', action="Edit",
                           add_quota=add_quota, form=form,
                           quota=quota, title="Edit Quota")



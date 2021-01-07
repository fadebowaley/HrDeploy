from flask import abort, flash, redirect, render_template, url_for, g, jsonify, current_app
from flask_login import current_user, login_required
import os
import secrets
from PIL import Image
from app.admin import bp
from app.admin.forms import DepartmentForm, EmployeeForm, EmergencyForm, CerpacForm, RoleForm, CompanyForm, PassportForm, QuotaForm, EmployeeAssignForm
from app import db
from app.models import Department, Employee, Emergency, Cerpac, Role, Company, Passport, Quota



@bp.route('/fullprofile', methods=['GET', 'POST'])
@login_required
def fullprofile():
    """
    this might require a join table to bind everything together
    A route and template designed to achieve this
    A profile to Display all full Display all tables in the Database Dynamically
    show_id
    =>Expartriate Details,
    =>Company-quota assigned,
    =>Passport details,
    =>Cerpac Details,
    =>History Details
    check_admin()
    passports = Passport.query.all()
    """
  


@bp.route('/cerpacditto', methods=['GET', 'POST'])
@login_required
def list_cerpacditto():
    """
    A fuction and route to Display all Cerpacs/Expartriates/Companies/Detaails dates and renewals/ Notify when Expired and Send email
    """
    check_admin()
    passports = Passport.query.all()



@bp.route('/reminder', methods=['GET', 'POST'])
@login_required
def list_remider():
    """
    List all Dates of reminders renewals/ Notify when Expired and Send email
    """
    check_admin()
    passports = Passport.query.all()


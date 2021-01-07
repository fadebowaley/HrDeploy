from datetime import datetime
from flask import abort, flash, redirect, render_template, url_for, g, jsonify, current_app
from flask_login import current_user, login_required
import os
import secrets
from hashlib import md5
from PIL import Image
from app.admin import bp
from app.admin.forms import DepartmentForm, EmployeeForm, EmergencyForm, CerpacForm, RoleForm, CompanyForm, PassportForm, QuotaForm, EmployeeAssignForm
from app import db
from app.auth.forms import RegistrationForm
from app.models import Department, Employee, Family, Cerpac, Role, Company, Passport, Quota, User


def  check_admin():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)


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
    =>History Details """
    

    check_admin()
    passports = Passport.query.all()
    check_admin()
    users = User.query.all()

    return render_template('admin/users/users.html',
                           users=users, title="users")
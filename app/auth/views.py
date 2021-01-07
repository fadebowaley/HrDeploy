from flask import render_template, redirect, url_for, flash, request, abort, send_from_directory
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import login_required, login_user, logout_user, current_user
import datetime
from datetime import datetime
from datetime import date, timedelta
import dateutil.relativedelta
import dateutil.parser
import dateutil.rrule
import calendar
#from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, UpdateAccountForm, \
     ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email, send_welcome_email
import os
from flask import current_app
import urllib.request
from werkzeug.utils import secure_filename
import secrets
from PIL import Image
#import imghdr


@bp.route('/register', methods=['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('home.profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User( email=form.email.data,
         username=form.username.data ,
         is_admin=form.is_admin.data,
         password=form.password.data)
        #user.set_password(form.password.data)
        # add user to the database
        db.session.add(user)
        db.session.commit()
        send_welcome_email(user)
        flash('You have successfully registered! Check your email.', category="your_error_argument")

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')



@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log user in
            login_user(user)

            # redirect to the appropriate dashboard page
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
            # redirect to the dashboard page after login
                return redirect(url_for('home.profile'))
              
        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))




@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home.profile'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.profile'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home.homepage'))
  
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #user.passwordUpdated_on = datetime.now()
        #user.password_hash = generate_password_hash(password) 
        password=form.password.data
        #user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/passports', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
    
 

@bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='passports/' + current_user.image_file)
    return render_template('auth/account.html', title='Account',
                           image_file=image_file, form=form)




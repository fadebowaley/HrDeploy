from flask import abort, render_template,flash, redirect, url_for, request
from flask_login import current_user, login_required
from app.home import bp
from app.models import  Token_serial, Lap
from app.home.forms import LapForm, MainForm
from app import db

@bp.route('/')
@bp.route('/index')
def homepage():
    return render_template('home/index2.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('home/profile.html', title="Profile")

 #add admin dashboard view
@bp.route('/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")


""" This route helps us determine what we are doing dynamically"""

@bp.route('/races', methods=['GET', 'POST'])
def add_race():
    form = MainForm()

    if form.validate_on_submit():
        # Create race
        new_race = Race()
        db.session.add(new_race)
        for lap in form.laps.data:
            new_lap = Lap(**lap)
            # Add to race
            new_race.laps.append(new_lap)
        db.session.commit()

    races = Race.query

    return render_template(
        'home/races/race.html',
        form=form,
        races=races
    )


@bp.route('/<race_id>', methods=['GET'])
def show_race(race_id):
    """Show the details of a race."""
    race = Race.query.filter_by(id=race_id).first()

    return render_template(
        'home/races/show.html',
        race=race
    )
#from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, IntegerField, StringField, \
        SubmitField


class LapForm(Form):
    """Subform.
    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    runner_name = StringField('Quota Position')
    #lap_time = IntegerField('Lap time')


class MainForm(FlaskForm):
    """Parent form."""
    laps = FieldList(
        FormField(LapForm),
        min_entries=1,
        max_entries=20
    )

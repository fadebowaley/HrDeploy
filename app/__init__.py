#third party import
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
#from flask_wtf.csrf import CsrfProtect
from faker import Faker
from flask import Flask, request, current_app
from flask_moment import Moment
#from flask_babel import Babel, lazy_gettext as _l
from config import Config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Bundle, Environment
from sqlalchemy.orm import sessionmaker

 # global scope  
Session = sessionmaker(autoflush=False)  

fake = Faker()
session = Session()
db = SQLAlchemy()
migrate = Migrate()
#csrf = CsrfProtect()
login = LoginManager()
login.login_view = 'auth.login'
#login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
#babel = Babel()

#Local imports
#from config import Config
#from config import app_config
# Set jinja template global
#app.jinja_env.globals['momentjs'] = momentjs

# Initialize the app
def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.pdf']
    app.config['UPLOADED_ITEMS_DEST'] = 'uploads'
    #app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'sta')
    
    db.init_app(app)
    #csrf.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    #babel.init_app(app)



    #Blue print for Admin , Auth and Home
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.ditto import bp as ditto_bp
    app.register_blueprint(ditto_bp)


    #loading the js file 
    js = Bundle('app.js', 'bootstrap-datetimepicker.min.js', 'bootstrap.min.js', 'chart.js', 'dataTables.bootstrap4.min.js', 'dropfiles.js','fullcalendar.min.js', 'jquery.ui.touch-punch.min.js', 'jquery.slimscroll.min.js', 'mask.js', 'moment.min.js', 'multiselect.min.js', 'popper.min.js', 'select2.min.js','main.js', 'task.js', 'jquery-3.2.1.min.js','jquery.ui.touch-punch.min.js','jquery.maskedinput.min.js','chart.js','jquery.dataTables.min.js',   output='gen/fade.js' )
    #js = Bundle('jquery-3.2.1.min.js', 'popper.min.js','bootstrap.min.js', 'jquery.slimscroll.min.js', 'app.js', '' )
    style_bundle=Bundle('bootstrap.min.css', 'font-awesome.min.css','line-awesome.min.css','style.css', 'select2.min.css','fullcalendar.min.css', 'font-awesome.min.css','dataTables.bootstrap4.min.css', 'bootstrap-datetimepicker.min.css',  output='gen/fade.css'  )
    assets = Environment(app)
    assets.register('main_js', js)
    assets.register('main_styles', style_bundle)



   
    return app

"""
#@babel.localeselector
#def get_locale():
    #return request.accept_languages.best_match(current_app.config['LANGUAGES'])

"""
from app import views, models


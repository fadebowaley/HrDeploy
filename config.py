import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


# class Config(object):
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'expartio.db')

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:root@/exparty'

    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    #MAIL_SERVER = os.environ.get('MAIL_SERVER')
    #MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    #MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    #MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #ADMINS = ['noreply@quickito.com']


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_SENDER ='noreply@local.host'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'frank.adebowale@gmail.com'
    MAIL_PASSWORD = 'possible12'
    ADMINS = ['	no-reply@expartkia.com']

    #Celery
    CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
    CELERY_ACCEPT_CONTENT =['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 5

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    
  


# Twilio settings
#export TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXX
#export TWILIO_AUTH_TOKEN=YYYYYYYYYYYYYYYYYY
#export TWILIO_NUMBER=+###########

    
    #LANGUAGES = ['en', 'es']
    #MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    #POSTS_PER_PAGE = 25
    #UPLOAD_FOLDER = 'static/uploads/'
    #UPLOAD_FOLDER = UPLOAD_FOLDER
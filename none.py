#import os
# secet key settings  
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'p9Bv<3Eid9%$i01'

#SQLALCHEMY_DATABASE_URI = 'mysql://dt_admin:dt2016@localhost/dreamteam_db'
#SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/nu.db'

#To use sqlite lite, Import os and enjoy
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'exparty.db')


SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config(object):
    # ...
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SECRET_KEY = "Your_secret_string"

class DevelopmentConfig(Config):
    """ Development configurations      """
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """ Production configurations   """
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
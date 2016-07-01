import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY                     = os.environ.get('SECRET_KEY')  or 'the owl and the pussycat'
    SQLALCHEMY_COMMIT_ON_TEARDOWN  = True
    SQLALCHEMY_DATABASE_URI        = os.path.join(basedir,'data.sqlite')
    FLASKY_MAIL_SUBJECT_PREFIX     = '[Flasky]'
    FLASKY_MAIL_SENDER             = 'Flasky Admin <flasky@exapmle.com>'
    FLASKY_ADMIN                   = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

    
    class DevelopmentConfig(Config):
        DEBUG = True

    config = {
        'development':  DevelopmentConfig
    }

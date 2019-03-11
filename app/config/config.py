class BaseConfig(object):
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Demian!89@localhost/specup"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    JWT_SECRET_KEY = 'dev'
    JWT_TOKEN_LOCATION = 'headers'
    JWT_ACCESS_TOKEN_EXPIRES = 1800

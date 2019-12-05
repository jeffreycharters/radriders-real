import os
class Config(object):
    SECREY_KEY = os.environ.get('SECRET_KEY')  or 'you-will-never-guess'
    
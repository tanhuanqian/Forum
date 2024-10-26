import os
HOSTNAME = 'localhost'
PORT     = '5432'
DATABASE = 'forum'
USERNAME = 'postgres'
PASSWORD = '1234'

# PostgreSQL 的连接 URI
DB_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

MAIL_SERVER = "smtp.gmail.com"
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_PORT = 587
MAIL_USERNAME = "tanhuanqian1@gmail.com"
MAIL_PASSWORD = "vvgxeodmoijxkhyu"
MAIL_DEFAULT_SENDER = "tanhuanqian1@gmail.com"
#vvgx eodm oijx khyu

# config.py
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')

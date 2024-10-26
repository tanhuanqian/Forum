import os

# PostgreSQL 的连接 URI
HOSTNAME = os.getenv('DB_HOST', 'localhost')
PORT = os.getenv('DB_PORT', '5432')
DATABASE = os.getenv('DB_NAME', 'forum')
USERNAME = os.getenv('DB_USER', 'postgres')
PASSWORD = os.getenv('DB_PASSWORD', '1234')

DB_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

MAIL_SERVER = "smtp.gmail.com"
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_PORT = 587
MAIL_USERNAME = os.getenv('MAIL_USERNAME', "tanhuanqian1@gmail.com")
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', "vvgxeodmoijxkhyu")
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', "tanhuanqian1@gmail.com")

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')

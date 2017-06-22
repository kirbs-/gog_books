import os
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database', 'app.db')
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/postgres'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'database', 'migrations')
OTP_SECRET = 'abc'
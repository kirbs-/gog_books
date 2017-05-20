from flask import Flask
from jinja2 import Environment
from hamlish_jinja import HamlishExtension, HamlishTagExtension
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'abc'
db = SQLAlchemy(app)

env = Environment(extensions=[HamlishExtension])
env.hamlish_file_extensions=('.haml', '.html.haml')
env.hamlish_enable_div_shortcut=True
app.jinja_env.add_extension(HamlishTagExtension)
app.jinja_env.add_extension(HamlishExtension)

from app import views, models

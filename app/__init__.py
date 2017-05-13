from flask import Flask
from jinja2 import Environment
from hamlish_jinja import HamlishExtension, HamlishTagExtension

app = Flask(__name__)

env = Environment(extensions=[HamlishExtension])
env.hamlish_file_extensions=('.haml', '.html.haml')
app.jinja_env.add_extension(HamlishTagExtension)
app.jinja_env.add_extension(HamlishExtension)

from app import views
import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required

from config import BaseConfig
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

def register_dashapps(app):
    from app.dashapp1.layout import layout
    from app.dashapp1.callbacks import register_callbacks
    from app import db 
    from app.models import User

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    dashapp1 = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/assets/',
                         meta_tags=[meta_viewport])

    with app.app_context():
        dashapp1.title = 'Dashapp 1'
        dashapp1.layout = layout
        register_callbacks(dashapp1)

    _protect_dashviews(dashapp1)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'd5e15dd080bab91ed0a457aef93f874b0308e35dbde833d9af6f44d888021f6c'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ffplcwjuwnchtz:d5e15dd080bab91ed0a457aef93f874b0308e35dbde833d9af6f44d888021f6c@ec2-54-83-192-245.compute-1.amazonaws.com:5432/da7cfdmp1uib8j'
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
register_dashapps(app)
from app import routes

# -*- coding: utf-8 -*-
import os

__version__ = '0.1'
from flask import Flask
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
import dotenv

def create_app():
	db.init_app(app)

	login_manager = LoginManager()
	login_manager.login_view = 'login'
	login_manager.init_app(app)

	from project.models.Model import User

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

CONFIG = dotenv.dotenv_values()
app = Flask('project')
app.config['SECRET_KEY'] = '\xe9\x11%\xd4\xd5ko\x1b:=:\x80\x8d0\t\xd4O\xd8\xd1R\xb3U\xdc'
app.debug = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+CONFIG['SQL_USERNAME']+':'+CONFIG['SQL_PASSWORD']+'@'+CONFIG['SQL_HOST']+':'+CONFIG['SQL_PORT']+'/'+CONFIG['SQL_DATABASE']
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)
create_app()
from project.controllers import *

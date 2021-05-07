# -*- coding: utf-8 -*-
import os

__version__ = '0.1'
from flask import Flask
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

def create_app():
	db.init_app(app)

	login_manager = LoginManager()
	login_manager.login_view = 'login'
	login_manager.init_app(app)

	from project.models.Model import User

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

app = Flask('project')
app.config['SECRET_KEY'] = 'random'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://norbert.d:TV91OJsBxBLgnMVb@ysjcs.net:3306/norbertdajnowski_restserver'
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)
create_app()
from project.controllers import *

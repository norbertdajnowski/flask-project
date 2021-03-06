# -*- coding: utf-8 -*-
from project import app, db
from project.models.Model import User, Image
from project.controllers.main import logos, images
from flask import Blueprint, render_template, request, Flask, Response, url_for, flash, redirect
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/login')
def login():
	#Check if already logged in
	if current_user.is_authenticated:
		return render_template('dashGallery.html', current_user=current_user, logos=logos, images=images)
	else:
		return render_template('loginIndex.html')

@app.route('/login', methods=["POST"])
def login_post():
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User.query.filter_by(email=email).first()
	
    # check if user exists
    # hash and compare to real password
	if not user or not check_password_hash(user.password, password):
		flash('Please check your login details and try again.')
		return redirect(url_for('login')) 

    # if checks passed then login user
	login_user(user, remember=remember)
	return render_template('dashGallery.html', current_user=current_user, logos=logos, images=images)


@app.route('/logout')
@login_required
def logout():
	logout_user() 
	return redirect(url_for('start'))
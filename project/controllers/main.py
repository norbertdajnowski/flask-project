# -*- coding: utf-8 -*-
from project import app, db
from project.models.Model import User, Image, Blog
from flask import render_template, request, jsonify, Flask, Response, redirect, url_for, send_from_directory, flash
from flask_login import login_required, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField
from wtforms.validators import DataRequired	
import dotenv		

#CONFIG SETUP
CONFIG = dotenv.dotenv_values()
base_url = CONFIG["BASE_URL"]
logos = Image.all(base_url + 'project/uploads/logos')
images = Image.all(base_url + 'project/uploads/gallery')

class CreateForm(FlaskForm):
    text = StringField('name', validators=[DataRequired()])


@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response

#Loading images for the gallery page
@app.route('/gallery')
def gallery():
	db.create_all()
	images = Image.all(base_url + 'project/uploads/gallery')
	return render_template('gallery.html', current_user=current_user, images=images, logos=logos)

#Admin gallery access
@app.route('/dashGallery')
@login_required
def dashGallery():
	return render_template('dashGallery.html', current_user=current_user, images=images, logos=logos)

#Admin blog access
@app.route('/dashBlog')
@login_required
def dashBlog():
	return render_template('dashBlog.html', current_user=current_user, images=images, logos=logos)

#Blog post method
@app.route('/postBlog', methods=['POST'])
@login_required
def postBlog():

	#Collecting all form input data
	title = request.form.get('titleInput')
	author = request.form.get('authorInput')
	content = request.form.get('descriptionInput')
	objDatetime = datetime.now()
	date = objDatetime.strftime('%Y-%m-%d %H:%M:%S')
	imageData = request.files['imageInput']
	filename = str(imageData).split("'") #Figuring out the filename of the image
	if filename[1] != "None":
		Image.uploadBlog(imageData, filename[1]) #Uploading image to blog folder

	#Entry data validated
	if len(title) > 249 or len(title) < 5: 
		flash('Something is wrong with the title!')
		return redirect(url_for('dashBlog'))

	if len(author) > 119 or len(author) < 2:
		flash('Something is wrong with the author field!')
		return redirect(url_for('dashBlog'))

	if len(content) > 3499 or len(content) < 10:
		flash('Something is wrong with the description!')
		return redirect(url_for('dashBlog'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
	new_blog = Blog(title=title, author=author, date=date, content=content, image=filename[1])

    # add the new user to the database
	db.session.add(new_blog)
	db.session.commit()

	flash('Post added Succesfully')
	return redirect(url_for('dashBlog')) #Redirect back to admin blog page

@app.route('/')
def start(): #Landing page method
	db.create_all()
	images = Image.all(base_url + 'project/uploads/gallery')
	return render_template('home.html', current_user=current_user, images=images, logos=logos) #Loads home page

#Loads blog page
@app.route('/blog')
def blog():
	blogs = Blog.query.order_by(Blog.id.desc()).all()
	return render_template('blog.html', current_user=current_user, blogs=blogs, logos=logos)

#Fetches a specific blog entry and requests for it to be displayed on blog post page
@app.route('/blogPost', methods=['POST','GET'])
def getBlog():
	print("success")
	id = request.args.get('id')
	blog = Blog.query.get(id)
	return render_template('blogPost.html', current_user=current_user, blog=blog, logos=logos)

#Admin image removal method
@app.route('/removeImg', methods=['POST'])
@login_required
def removeImg():
	global images
	Image.remove(request.form.get('filename'))
	images = Image.all(base_url + 'project/uploads/gallery')
	return render_template('dashGallery.html', current_user=current_user, logos=logos, images=images)

#Admin image upload method
@app.route('/uploadImg', methods=['POST'])
@login_required
def uploadImg():
	global images
	file = request.files['file1']
	Image.upload(file)
	images = Image.all(base_url + 'project/uploads/gallery')
	return render_template('dashGallery.html', current_user=current_user, logos=logos, images=images)

#Fetching images

@app.route('/uploads/gallery/<path:filename>')
def gallery_static(filename):
    return send_from_directory(base_url + 'project/uploads/gallery', filename)


@app.route('/uploads/logos/<path:filename>')
def logos_static(filename):
    return send_from_directory(base_url + 'project/uploads/logos', filename)


@app.route('/uploads/blog/<path:filename>')
def blog_static(filename):
	return send_from_directory(base_url + 'project/uploads/blog', filename)

#logged in checker
def noLogon():
	if current_user.is_authenticated:
		pass
	else:
		return redirect(url_for('login'))


@app.route('/upload', methods=['POST'])
def upload():
    current_app.logger.info('uploading')
    if request.method == 'POST' and 'image' in request.files:
        image = Image('', post=request.files['image'], root=current_app.config['GALLERY_ROOT_DIR'])

        if image.path.suffix in current_app.config['UPLOAD_ALLOWED_EXTENSIONS']:
            return ("ok", 201,)

        current_app.logger.info('failed to upload')

    return (jsonify({'error': 'you need to pass an image'}), 400)



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

logos = Image.all('D:/ProgramData/Third Year - SEM 2/Advanced Web/rest-server/flask-mvc/project/uploads/logos')
images = Image.all('D:/ProgramData/Third Year - SEM 2/Advanced Web/rest-server/flask-mvc/project/uploads/gallery')

class CreateForm(FlaskForm):
    text = StringField('name', validators=[DataRequired()])


@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response


@app.route('/')
def start():
	db.create_all()
	images = Image.all('D:/ProgramData/Third Year - SEM 2/Advanced Web/rest-server/flask-mvc/project/uploads/gallery')
	return render_template('gallery.html', current_user=current_user, images=images, logos=logos)

@app.route('/dashGallery')
@login_required
def dashGallery():
	return render_template('dashGallery.html', current_user=current_user, images=images, logos=logos)

@app.route('/dashBlog')
@login_required
def dashBlog():
	return render_template('dashBlog.html', current_user=current_user, images=images, logos=logos)

@app.route('/postBlog', methods=['POST'])
@login_required
def postBlog():

	title = request.form.get('titleInput')
	author = request.form.get('authorInput')
	image = request.form.get('imageInput')
	content = request.form.get('descriptionInput')
	objDatetime = datetime.now()
	date = objDatetime.strftime('%Y-%m-%d %H:%M:%S')

	if len(title) > 249 or len(title) < 10: # if a user is found, we want to redirect back to signup page so user can try again
		flash('Something is wrong with the title!')
		return redirect(url_for('dashBlog'))

	if len(author) > 119 or len(author) < 5:
		flash('Something is wrong with the author field!')
		return redirect(url_for('dashBlog'))

	if len(image) > 119:
		flash('Something is wrong with the image filename')
		return redirect(url_for('dashBlog'))

	if len(content) > 3499 or len(content) < 10:
		flash('Something is wrong with the description!')
		return redirect(url_for('dashBlog'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
	new_blog = Blog(title=title, author=author, date=date, content=content, image=image)

    # add the new user to the database
	db.session.add(new_blog)
	db.session.commit()

	flash('Post added Succesfully')
	return redirect(url_for('dashBlog'))

@app.route('/about')
def about():
	pass


@app.route('/blog')
def blog():
	blogs = Blog.query.order_by(Blog.id.desc()).all()
	return render_template('blog.html', current_user=current_user, blogs=blogs, logos=logos)


@app.route('/blogPost', methods=['POST','GET'])
def getBlog():
	print("success")
	id = request.args.get('id')
	blog = Blog.query.get(id)
	return render_template('blogPost.html', current_user=current_user, blog=blog, logos=logos)

@app.route('/removeImg', methods=['POST'])
def removeImg():
	global images
	Image.remove(request.form.get('filename'))
	images = Image.all('D:/ProgramData/Third Year - SEM 2/Advanced Web/rest-server/flask-mvc/project/uploads/gallery')
	return render_template('dashGallery.html', current_user=current_user, logos=logos, images=images)

@app.route('/uploadImg', methods=['POST'])
def uploadImg():
	global images
	file = request.files['file1']
	print(file)
	Image.upload(file)
	images = Image.all('D:/ProgramData/Third Year - SEM 2/Advanced Web/rest-server/flask-mvc/project/uploads/gallery')
	return render_template('dashGallery.html', current_user=current_user, logos=logos, images=images)

@app.route('/uploads/gallery/<path:filename>')
def gallery_static(filename):
    return send_from_directory('D:/ProgramData/Third Year - SEM 2/Advanced Web/rest-server/flask-mvc/project/uploads/gallery', filename)


@app.route('/uploads/logos/<path:filename>')
def logos_static(filename):
    return send_from_directory('D:/ProgramData/Third Year - SEM 2/Advanced Web/rest-server/flask-mvc/project/uploads/logos', filename)


@app.route('/uploads/blog/<path:filename>')
def blog_static(filename):
	pass


@app.route('/print', methods=['GET','POST'])
def printer():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        from project.models.Printer import Printer
        printer = Printer()
        printer.show_string(form.text.data)
        return render_template('printer/index.html')
    return render_template('printer/print.html', form=form)


@app.route("/dbsend", methods=['POST'])
def sendData():
	data = request.form
	return jsonify(data)


@app.route("/dbget", methods=['GET'])
@login_required
def getData():
	users = User.query.all()
	return render_template("printer/queryAll.html", users=users)


def noLogon():
	if current_user.is_authenticated:
		return ''
	else:
		return redirect(url_for('login'))


@app.route('/upload', methods=['POST'])
def upload():
    current_app.logger.info(f'uploading')
    if request.method == 'POST' and 'image' in request.files:
        image = Image('', post=request.files['image'], root=current_app.config['GALLERY_ROOT_DIR'])

        if image.path.suffix in current_app.config['UPLOAD_ALLOWED_EXTENSIONS']:
            return ("ok", 201,)

        current_app.logger.info(f'failed to upload {image!r}')

    return (jsonify({'error': 'you need to pass an image'}), 400)



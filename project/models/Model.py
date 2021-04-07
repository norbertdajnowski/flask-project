# -*- coding: utf-8 -*-
import os, sys
from flask import flash
from flask_login import UserMixin
from pathlib import Path
from project import app, db
from flask_sqlalchemy import SQLAlchemy

class User(UserMixin, db.Model):

	def __init__(self, username, email, password, name):
		self.username = username
		self.email = email
		self.password = password
		self.name = name

	def __repr__(self):
		return '{"User": "%r"}' % self.username

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(100), unique=True, nullable=False)
	name = db.Column(db.String(1000), unique=False, nullable=False)
	
class Blog(db.Model):

    def __init__(self, arg):
        super(Blog, self).__init__()
        self.arg = arg

    def __repr__(self):
        return '{"Title": "%r"}' % self.title

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=False, nullable=False)
    author = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.DateTime(), unique=False, nullable=False)
    content = db.Column(db.String(3500), unique=False, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=True)
        

class FilesystemObjectDoesNotExist(Exception):
    pass


class FilesystemObject(object):



    def __init__(self, filename, post=None, root=None):
        """Create an object from the information of the given filename or from a
        uploaded file.

        Example of usage:

            if request.method == 'POST' and 'photo' in request.POST:
                f = FilesystemObject('cats.png', request.POST['photo'])

        """
        catTag =['foo, des, eve']

        self.root_dir = Path(root)
        self.path = Path(filename if not post else secure_filename(post.filename))
        self.abspath = self.root_dir / self.path
        catList = str(self.path).split('.')
        self.category = catList[1]


        if post:
            self.upload(post)

        try:
            stats = os.stat(self.abspath)
            self.timestamp = stats.st_mtime
        except IOError as e:
            current_app.logger.error(e)
            current_app.logger.error(f'{self!r}')
            raise FilesystemObjectDoesNotExist(e)

    def __repr__(self):
        return f'<{self.__class__.__name__}(filename={self.path}, root={self.root_dir})>'

    def upload(post):
        absolutePath = "D:/ProgramData/Third Year - SEM 2/Advanced Web/rest-server/flask-mvc/project/uploads/gallery/"
        """Get a POST file and save it to the settings.GALLERY_ROOT_DIR"""
        # TODO: handle filename conflicts
        # http://flask.pocoo.org/docs/patterns/fileuploads/
        print('saving at ' + absolutePath)
        post.save(str(absolutePath))

    def remove(file):
        absolutePath = "D:/ProgramData/Third Year - SEM 2/Advanced Web/rest-server/flask-mvc/project/uploads/gallery/"
        filename = file.split('/')
        file = absolutePath + filename[len(filename) - 1]
        print(file)
        try:
            if os.path.exists(file):
                print("image removed")
                os.remove(file)
            else:
                print("File does not exist")
        except:
            print("Error occured at image removal")

    @classmethod
    def all(cls, root):
        """Return a list of files contained in the directory pointed by settings.GALLERY_ROOT_DIR.
        """
        return [cls(filename=x, root=root) for x in os.listdir(root)]


class Image(FilesystemObject):
    pass

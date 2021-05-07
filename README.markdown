Submission for my Advanced Web Development Module -  3CB109

github link: https://github.com/norbertdajnowski/flask-project

Working example: http://ysjcs.net:5017/

A simple Catering REST application, featuring a gallery (Sorted by categories and order of upload), blog entries, and a landing page with details about the organisation. Also the application contains a full dashboard for the admin to add or delete images and blogs.

-- STEPS TO LAUNCH --

1) Modifying the config files

i) runserver.py - Change host and port values to your settings

    HOST: Name of the server that you are hosting your application on

    PORT: Port number on the server to setup Flask on

ii) .env - Enter your MySQL details and base path

    BASE_URL: Enter the base path leading to your "project" folder

    SQL_HOST: Your database host

    SQL_USERNAME: MySQL username

    SQL_PASSWORD: MySQL password

    SQL_DATABASE: MySQL database name

    SQL_PORT: MySQL port for connection


2) Install the required libraries using the following command

    pip install -r requirements.txt

Optional:

    pip install --upgrade -r requirements.txt


3)Use the following command to start the application

    python runserver.py



-- SITE NAVIGATION --

Normal client will have access to Home>Gallery>Blog>BlogPosts>Login

Home - Landing page with space for information about your company

Gallery - Display of uploaded images

Blog - Display of blog entries

Login - You can find the link to dashboard login in the footer "Dashboard"

-- ADMIN --

Gallery Dashboard - Upload/Remove images (Click on images to select them and remove)

Blog Dashboard - Enter all of the required details to make a blog entry
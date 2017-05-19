from app import app, models
from flask import render_template
from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)

@app.route('/')
@app.route('/index')
def index():
    books = models.Book.query.all()
    return render_template('index.haml', books=books)

@app.route('/highes_rated')
def highest_rated():
    books = models.Book.highest_rated()
    return render_template('index.haml', books=books)


from app import app, models
from flask import render_template, request
from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)

@app.route('/')
@app.route('/index')
def index():
    books = models.Book.query.all()
    return render_template('index.haml', books=books)

@app.route('/sort', methods=['GET','POST'])
def highest_rated():
    sort_type = request.form['sortby']
    print(request)
    return render_template('index.haml', books=models.Book.sort(sort_type))


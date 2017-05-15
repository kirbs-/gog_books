from app import app, models
from flask import render_template
from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)

@app.route('/')
@app.route('/index')
def index():
    # books = [{"cover_url": "https://images-na.ssl-images-amazon.com/images/I/513erhF-l2L._SY346_.jpg"}]
    books = models.Book.query.all()
    return render_template('index.haml', books=books)

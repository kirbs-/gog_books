from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    books = [{"cover_url": "https://images-na.ssl-images-amazon.com/images/I/513erhF-l2L._SY346_.jpg"}]
    return render_template('index.haml', books=books)

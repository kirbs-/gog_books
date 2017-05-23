from app import app, models
import config
from flask import render_template, request, redirect, abort, flash, jsonify
from flask_uploads import UploadSet, IMAGES
import onetimepass
import time


photos = UploadSet('photos', IMAGES)

@app.route('/')
@app.route('/index')
def index():
    books = [book.serialize() for book in models.Book.query.limit(2).all()]
    return render_template('index.haml', books=books)

@app.route('/sort', methods=['GET','POST'])
def highest_rated():
    sort_type = request.form['sortby']
    return render_template('index.haml', books=models.Book.sort(sort_type))

@app.route('/new/<show_num>/<token>')
def new_show(show_num, token):
    if onetimepass.valid_totp(token, config.OTP_SECRET):
        show = models.Show("http://gog.show/{}".format(show_num))
        show.save_books()
        flash('Added {} books.'.format(len(show.books)))
        return redirect('/')
    else:
        time.sleep(15)
        return abort(401)


@app.route('/new/<show_num>')
def new_show1(show_num):
    show = models.Show("http://gog.show/{}".format(show_num))
    show.save_books()
    return redirect('/')


@app.route('/fetch/<int:count>/<sort_type>/<int:size>')
def fetch(count, sort_type, size):
    # return jsonify([book.serialize() for book in models.Book.fetch(count, sort_type, size)])
    return render_template('books.haml', books=models.Book.fetch(count, sort_type, size))
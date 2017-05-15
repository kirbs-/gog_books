from app import db
from flask_uploads import UploadSet, IMAGES, configure_uploads
import requests
from werkzeug.datastructures import FileStorage
import app
from bs4 import BeautifulSoup


# UPLOADED_PHOTOS_DEST = '/app/static/images'
# photos = UploadSet('photos', IMAGES)
# configure_uploads(app.app, photos)

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True, unique=True)
    url = db.Column(db.String(1000), index=True, unique=True)
    number = db.Column(db.Integer)
    books = db.relationship('Book', backref='show', lazy='dynamic')

    def __init__(self, url):
        self.url = url

    @property
    def page(self):
        return requests.get(self.url)

    @property
    def book_links(self):
        out = []
        soup = BeautifulSoup(self.page.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            try:
                if 'amzn' in link['href']:
                    out.append(link['href'])
                    print link
            except:
                pass
        return out

    def save_books(self):
        for link in self.book_links:
            self.books.append(Book(link))

        db.session.commit()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    name = db.Column(db.String(500), index=True, unique=True)
    url = db.Column(db.String(1000), index=True, unique=True)
    cover_url = db.Column(db.String(1000), index=True, unique=True)
    # covers = db.relationship('Photo', backref='book', lazy='dynamic')

    def __init__(self, url):
        self.url = url
        # photo_filename = photos.save(FileStorage(requests.get(cover_url).content))
        # self.covers = [Photo(self.id, photo_filename)]

    @property
    def page(self):
        return requests.get(self.url)

    @property
    def cover(self):
        if not self.cover_url:
            soup = BeautifulSoup(self.page.text, 'html.parser')
            self.cover_url = soup.find('div', {'id': 'ebooksImageBlock'}).find_all_next('img')[0]['src']
            db.session.commit()
        return self.cover_url


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    filename = db.Column(db.String(1000), index=True, unique=True)

    def __init__(self, book_id, filename):
        self.book_id = book_id
        self.filename = filename

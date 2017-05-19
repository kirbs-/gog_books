from app import db
from flask_uploads import UploadSet, IMAGES, configure_uploads
import requests, xmltodict
from werkzeug.datastructures import FileStorage
import app
from bs4 import BeautifulSoup


# UPLOADED_PHOTOS_DEST = '/app/static/images'
# photos = UploadSet('photos', IMAGES)
# configure_uploads(app.app, photos)

GOODREADS_API_KEY = 'IM6ZFnKSuYfT44hZBS92Q'

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
    ratings = db.relationship('Rating', backref='book', lazy='dynamic')
    isbn10 = db.Column(db.String(1000), index=True, unique=True)
    isbn13 = db.Column(db.String(1000), index=True, unique=True)
    goodreads_book_id = db.Column(db.String(1000), index=True, unique=True)
    description = db.Column(db.String(4000), index=True, unique=True)
    # covers = db.relationship('Photo', backref='book', lazy='dynamic')

    def __init__(self, url):
        self.url = url
        # photo_filename = photos.save(FileStorage(requests.get(cover_url).content))
        # self.covers = [Photo(self.id, photo_filename)]

    @staticmethod
    def highest_rated():
        return Book.query.join(Rating).filter_by(source='amazon').order_by(Rating.value)

    @property
    def isbn(self):
        if not self.isbn10:
            soup = BeautifulSoup(self.page.text, 'html.parser')
            for ele in soup.find(id='productDetailsTable').find_all('li'):
                if 'ASIN' in ele.text:
                    self.isbn10 = ele.text.split()[1]
                    db.session.commit()
                    break

        return self.isbn10

    @property
    def goodreads_id(self):
        if not self.goodreads_book_id:
            url = 'https://www.goodreads.com/book/isbn_to_id'
            self.goodreads_book_id = requests.get(url, params={'key': GOODREADS_API_KEY, 'isbn': self.isbn}).text
        return self.goodreads_book_id

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

    @property
    def amazon_rating(self):
        rating = Rating.query.filter_by(book_id=self.id, source='amazon').first()

        if not rating:
            soup = BeautifulSoup(self.page.text, 'html.parser')
            amazon_rating = soup.find(id='acrPopover').get('title').split()[0]
            amazon_review_count = soup.find(id='acrCustomerReviewText').text.split()[0].replace(',', '')
            self.ratings.append(Rating('amazon', amazon_rating, amazon_review_count))
            db.session.commit()
            rating = Rating.query.filter_by(book_id=self.id, source='amazon').first()

        return rating

    @property
    def amazon_stars(self):
        return self.amazon_rating.value

    @property
    def amazon_reviews(self):
        return self.amazon_rating.review_count

    @property
    def goodreads_rating(self):
        rating = Rating.query.filter_by(book_id=self.id, source='goodreads').first()

        if not rating:
            json = xmltodict.parse(requests.get('https://www.goodreads.com/book/show', params={'key': GOODREADS_API_KEY, 'id': self.goodreads_id}).text)
            book_response = json['GoodreadsResponse']['book']
            self.ratings.append(Rating('goodreads', book_response['average_rating'], book_response['ratings_count']))
            self.description = book_response['description']
            db.session.commit()
            rating = Rating.query.filter_by(book_id=self.id, source='goodreads').first()

        return rating

    @property
    def goodreads_stars(self):
        return self.goodreads_rating.value

    @property
    def goodreads_reviews(self):
        return self.goodreads_rating.review_count


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    filename = db.Column(db.String(1000), index=True, unique=True)

    def __init__(self, book_id, filename):
        self.book_id = book_id
        self.filename = filename


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    source = db.Column(db.String(500), index=True, unique=True)
    value = db.Column(db.Float, index=True, unique=True)
    review_count = db.Column(db.Integer, index=True, unique=True)

    def __init__(self, source, value, review_count):
        self.source = source
        self.value = value
        self.review_count = review_count


# class Author(db.Model):



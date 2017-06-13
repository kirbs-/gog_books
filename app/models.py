from app import db
from flask_uploads import UploadSet, IMAGES, configure_uploads
import requests, xmltodict, traceback
from werkzeug.datastructures import FileStorage
import app
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# UPLOADED_PHOTOS_DEST = '/app/static/images'
# photos = UploadSet('photos', IMAGES)
# configure_uploads(app.app, photos)

GOODREADS_API_KEY = 'IM6ZFnKSuYfT44hZBS92Q'


def default_no_reviews(func):
    def wrapper(self):
        try:
            return func(self)
        except:
            return 'None'

    return wrapper


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True)
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

        db.session.add(self)
        db.session.commit()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    name = db.Column(db.String(500), index=True)
    url = db.Column(db.String(1000), index=True)
    cover_url = db.Column(db.String(1000), index=True)
    ratings = db.relationship('Rating', backref='book', lazy='dynamic')
    isbn10 = db.Column(db.String(1000), index=True, unique=True)
    isbn13 = db.Column(db.String(1000), index=True, unique=True)
    goodreads_book_id = db.Column(db.String(1000), index=True)
    description = db.Column(db.String(4000), index=True)
    # covers = db.relationship('Photo', backref='book', lazy='dynamic')

    def __init__(self, url):
        self.url = url
        self.amazon_rating
        self.goodreads_rating
        self.cover
        # photo_filename = photos.save(FileStorage(requests.get(cover_url).content))
        # self.covers = [Photo(self.id, photo_filename)]

    @staticmethod
    def sort(sort_by):
        if sort_by == 'Highest Rating':
            return Book.highest_rated()
        elif sort_by == 'Newest':
            return Book.newest()
        elif sort_by == 'Most Reviews':
            return Book.most_reviewed()
        elif sort_by == 'Author':
            return Book.authors_asc()
        else:
            raise ValueError('Unknown sorting: {}'.format(sort_by))

    @staticmethod
    def highest_rated():
        return Book.query.filter(Book.isbn10.isnot(None)).join(Rating).filter_by(source='amazon', ).order_by(Rating.value.desc(), Book.id).all()

    @staticmethod
    def most_reviewed():
        return Book.query.filter(Book.isbn10.isnot(None)).join(Rating).filter_by(source='amazon').order_by(Rating.review_count.desc(), Book.id).all()

    @staticmethod
    def newest():
        return Book.query.filter(Book.isbn10.isnot(None)).join(Show).order_by(Show.url.desc(), Book.id).all()

    @staticmethod
    def authors_asc():
        return Book.query.order_by(Book.author)

    @property
    @default_no_reviews
    def isbn(self):
        if not self.isbn10:
            soup = BeautifulSoup(self.page.text, 'html.parser')
            for ele in soup.find(id='productDetailsTable').find_all('li'):
                if 'ASIN' in ele.text or 'ISBN-10' in ele.text:
                    self.isbn10 = ele.text.split()[1]
                    db.session.commit()
                    break

        return self.isbn10

    @property
    @default_no_reviews
    def goodreads_id(self):
        if not self.goodreads_book_id and self.isbn:
            url = 'https://www.goodreads.com/book/isbn_to_id'
            result = requests.get(url, params={'key': GOODREADS_API_KEY, 'isbn': self.isbn}).text
            if result != '16173270': # default goodreads book id
                self.goodreads_book_id = result
        return self.goodreads_book_id

    @property
    def page(self):
        return requests.get(self.url, headers={'User-Agent': UserAgent().random})


    @property
    @default_no_reviews
    def cover(self):
        if not self.cover_url:
            soup = BeautifulSoup(self.page.text, 'html.parser')
            try:
                self.cover_url = soup.find('div', {'id': 'ebooksImageBlock'}).find_all_next('img')[0]['src']
            except AttributeError:
                self.cover_url = soup.find('div', {'id': 'imageBlock'}).find_all_next('img')[0]['src']
            db.session.commit()
        return self.cover_url

    @property
    def amazon_rating(self):
        rating = Rating.query.filter_by(book_id=self.id, source='amazon').first()

        if not rating:
            try:
                soup = BeautifulSoup(self.page.text, 'html.parser')
                amazon_rating = soup.find(id='acrPopover').get('title').split()[0]
                amazon_review_count = soup.find(id='acrCustomerReviewText').text.split()[0].replace(',', '')
                self.ratings.append(Rating('amazon', amazon_rating, amazon_review_count))
                db.session.commit()
                rating = Rating.query.filter_by(book_id=self.id, source='amazon').first()
            except:
                print "Error fetching amazon metadata: {}".format(self.url)
                traceback.print_exc()

        return rating

    @property
    @default_no_reviews
    def amazon_stars(self):
        return self.amazon_rating.value

    @property
    @default_no_reviews
    def amazon_reviews(self):
        return self.amazon_rating.review_count

    @property
    def goodreads_rating(self):
        rating = Rating.query.filter_by(book_id=self.id, source='goodreads').first()

        if not rating:
            try:
                json = xmltodict.parse(requests.get('https://www.goodreads.com/book/show', params={'key': GOODREADS_API_KEY, 'id': self.goodreads_id}).text)
                book_response = json['GoodreadsResponse']['book']
                self.ratings.append(Rating('goodreads', book_response['average_rating'], book_response['ratings_count']))
                self.description = book_response['description']
                db.session.commit()
                rating = Rating.query.filter_by(book_id=self.id, source='goodreads').first()
            except:
                print "Error fetching goodreads metadata: {}".format(self.url)
                traceback.print_exc()

        return rating

    @property
    @default_no_reviews
    def goodreads_stars(self):
        return self.goodreads_rating.value

    @property
    @default_no_reviews
    def goodreads_reviews(self):
        return self.goodreads_rating.review_count

    @staticmethod
    def fetch(book_count, sort_type, size):
        books = Book.sort(sort_type)[book_count: (book_count + size)]
        print books
        return books
    def serialize(self):
        return {'amazon_stars': self.amazon_stars,
                'amazon_reviews': self.amazon_reviews,
                'goodreads_id': self.goodreads_id,
                'goodreads_stars': self.goodreads_stars,
                'goodreads_reviews': self.goodreads_reviews,
                'cover': self.cover}


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
    source = db.Column(db.String(500), index=True)
    value = db.Column(db.Float, index=True)
    review_count = db.Column(db.Integer, index=True)

    def __init__(self, source, value, review_count):
        self.source = source
        self.value = value
        self.review_count = review_count


# class Author(db.Model):




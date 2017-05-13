from app import db


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True, unique=True)
    url = db.Column(db.String(1000), index=True, unique=True)
    number = db.Column(db.Integer)
    books = db.relationship('Book', backref='show', lazy='dynamic')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    name = db.Column(db.String(500), index=True, unique=True)
    url = db.Column(db.String(1000), index=True, unique=True)
    cover_url = db.Column(db.String(1000), index=True, unique=True)
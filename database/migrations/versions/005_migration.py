from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
book = Table('book', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('show_id', Integer),
    Column('name', String(length=500)),
    Column('url', String(length=1000)),
    Column('cover_url', String(length=1000)),
    Column('isbn10', String(length=1000)),
    Column('isbn13', String(length=1000)),
    Column('goodreads_book_id', String(length=1000)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].columns['goodreads_book_id'].create()
    post_meta.tables['book'].columns['isbn10'].create()
    post_meta.tables['book'].columns['isbn13'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].columns['goodreads_book_id'].drop()
    post_meta.tables['book'].columns['isbn10'].drop()
    post_meta.tables['book'].columns['isbn13'].drop()

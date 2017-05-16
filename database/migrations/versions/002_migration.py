from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
photo = Table('photo', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('book_id', Integer),
    Column('filename', String(length=1000)),
)

book = Table('book', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('show_id', INTEGER),
    Column('name', VARCHAR(length=500)),
    Column('url', VARCHAR(length=1000)),
    Column('cover_url', VARCHAR(length=1000)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['photo'].create()
    pre_meta.tables['book'].columns['cover_url'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['photo'].drop()
    pre_meta.tables['book'].columns['cover_url'].create()

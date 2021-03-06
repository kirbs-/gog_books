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
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].columns['cover_url'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book'].columns['cover_url'].drop()

import logging
logging.basicConfig(level=logging.DEBUG)
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from whcfix.data.models import Base


# The driver that talks to the db
engine = create_engine('sqlite:///:memory:', echo=True, convert_unicode=True)


# A session class that the application can user to talk to the driver
Session = sessionmaker(engine)


def init_db():
    Base.metadata.create_all(engine)

def test_post():
    from whcfix.data.models import Post
    p = Post(title='Hello', body='World')
    s = Session()
    s.add(p)
    s.commit()
    print s.query(Post).all()


if __name__ == '__main__':
    init_db()
    test_post()

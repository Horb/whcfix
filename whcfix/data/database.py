from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from whcfix.data.models import Base
import whcfix.settings as settings
from contextlib import contextmanager

# The driver that talks to the db
engine = create_engine(settings.CONNECTION_STRING, echo=True, convert_unicode=True)

# A session class that the application can user to talk to the driver
Session = scoped_session(sessionmaker(engine))

def init_db():
    Base.metadata.create_all(engine)

@contextmanager
def get_db():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def test_post():
    from whcfix.data.models import Post
    p = Post(title='Hello', body='World')
    s = Session()
    s.add(p)
    s.commit()
    print s.query(Post).all()

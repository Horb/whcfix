from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# A base class such that models can be declared in the application
Base = declarative_base()

class Post(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)

    def __repr__(self):
        return "<Post (title='%s')>" % self.title

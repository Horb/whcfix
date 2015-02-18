from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

# A base class such that models can be declared in the application
Base = declarative_base()

class Post(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    is_published = Column(Boolean, nullable=False)
    first_published_date = Column(DateTime)
    

    def __repr__(self):
        return "<Post (title='%s')>" % self.title

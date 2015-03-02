import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text

# A base class such that models can be declared in the application
Base = declarative_base()


class Post(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    body = Column(Text)
    is_published = Column(Boolean, nullable=False)
    first_published_date = Column(DateTime)
    
    def __repr__(self):
        return "<Post (id='%s' title='%s')>" % (self.id, self.title)

    def publish(self):
        self.is_published = True
        if self.first_published_date is None:
            self.first_published_date = datetime.datetime.now()

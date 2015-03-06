import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey

# A base class such that models can be declared in the application
Base = declarative_base()


class Post(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    body = Column(Text)
    is_published = Column(Boolean, nullable=False)
    first_published_date = Column(DateTime)
    image_file_name = Column(String(250))
    signature = Column(String(250))
    
    def __repr__(self):
        return "<Post (id='%s' title='%s')>" % (self.id, self.title)

    def publish(self):
        self.is_published = True
        if self.first_published_date is None:
            self.first_published_date = datetime.datetime.now()

    __mapper_args__ = {
            'polymorphic_identity' : 'post',
            }

class MatchReport(Base):

    __tablename__ = 'matchreports'

    id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    home = Column(String(250))
    away = Column(String(250))
    push_back = Column(DateTime)

    __mapper_args__ = {
            'polymorphic_identity' : 'match_report',
            }


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

    def unpublish(self):
        self.is_published = False

    def publish(self):
        self.is_published = True
        if self.first_published_date is None:
            self.first_published_date = datetime.datetime.now()

    __mapper_args__ = {
            'polymorphic_identity' : 'post',
            }


def match_reports_for(team, db):
    match_reports = db.query(MatchReport).all()
    match_reports = [mr for mr in match_reports if mr.doesFeature(team)]
    match_reports.sort(key=lambda mr: mr.push_back)
    match_reports.reverse()
    return match_reports

class MatchReport(Post):

    __tablename__ = 'matchreports'

    id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    home = Column(String(250))
    away = Column(String(250))
    push_back = Column(DateTime)

    __mapper_args__ = {
            'polymorphic_identity' : 'match_report',
            }

    def doesFeature(self, team):
        r = team in (self.home, self.away)
        return r 

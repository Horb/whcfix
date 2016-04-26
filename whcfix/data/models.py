from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey

# A base class such that models can be declared in the application
Base = declarative_base()


class Tournament(Base):

    __tablename__ = 'tournaments'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))


class Division(Base):

    __tablename__ = 'divisions'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))

    teams = relationship("Team", back_populates="division")


class Team(Base):

    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    division_id = Column(Integer, ForeignKey('divisions.id'))

    division = relationship("Division", back_populates="teams")

    home_fixtures = relationship("Fixture", back_populates="home_team", primaryjoin="Team.id==Fixture.home_team_id")
    away_fixtures = relationship("Fixture", back_populates="away_team", primaryjoin="Team.id==Fixture.away_team_id")


class Venue(Base):

    __tablename__ = "venues"

    id = Column(Integer, primary_key=True)
    name = Column(String(250))

    fixtures = relationship("Fixture", back_populates="venue")


class Fixture(Base):

    __tablename__ = "fixtures"
    id = Column(Integer, primary_key=True)
    push_back = Column(DateTime)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    venue_id = Column(Integer, ForeignKey("venues.id"))

    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_fixtures")
    away_team = relationship("Team",  foreign_keys=[away_team_id], back_populates="away_fixtures")
    venue = relationship("Venue", back_populates="fixtures")

    result = relationship("Result")

class Result(Base):
    
    __tablename__ = 'results'
    fixture_id = Column(Integer, ForeignKey("fixtures.id"), primary_key=True)
    home_goals = Column(Integer)
    away_goals = Column(Integer)
    fixture = relationship("Fixture")


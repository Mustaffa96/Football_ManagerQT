from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    position = Column(String(50))
    nationality = Column(String(100))
    team_id = Column(Integer, ForeignKey('teams.id'))
    
    # Stats
    attack = Column(Integer)
    defense = Column(Integer)
    stamina = Column(Integer)
    speed = Column(Integer)
    technique = Column(Integer)
    
    # Contract details
    wage = Column(Float)
    value = Column(Float)
    contract_end = Column(Date)
    
    # Relationships
    team = relationship("Team", back_populates="players")

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100))
    league = Column(String(100))
    budget = Column(Float)
    
    # Relationships
    players = relationship("Player", back_populates="team")
    tactics = relationship("TeamTactics", back_populates="team")
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")

class TeamTactics(Base):
    __tablename__ = 'team_tactics'
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    name = Column(String(100))  # e.g., "Default", "Attacking", "Defensive"
    formation = Column(String(50))  # e.g., "4-4-2", "4-3-3"
    player_positions = Column(JSON)  # Store player positions as JSON
    player_roles = Column(JSON)  # Store player roles as JSON
    
    # Relationships
    team = relationship("Team", back_populates="tactics")

class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    home_team_id = Column(Integer, ForeignKey('teams.id'))
    away_team_id = Column(Integer, ForeignKey('teams.id'))
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    date = Column(Date)
    status = Column(String(20))  # "scheduled", "in_progress", "completed"
    possession = Column(JSON)  # Store possession stats
    shots = Column(JSON)  # Store shot stats
    
    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    events = relationship("MatchEvent", back_populates="match")

class MatchEvent(Base):
    __tablename__ = 'match_events'
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    minute = Column(Integer)
    event_type = Column(String(50))  # "goal", "shot", "foul", "card", etc.
    player_id = Column(Integer, ForeignKey('players.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))
    details = Column(JSON)  # Additional event details
    
    # Relationships
    match = relationship("Match", back_populates="events")
    player = relationship("Player")
    team = relationship("Team")

def init_db():
    """Initialize the database and create tables"""
    import os
    
    # Remove existing database file if it exists
    db_file = 'football_manager.db'
    if os.path.exists(db_file):
        os.remove(db_file)
    
    engine = create_engine('sqlite:///football_manager.db')
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Create a new database session"""
    engine = create_engine('sqlite:///football_manager.db')
    Session = sessionmaker(bind=engine)
    return Session()

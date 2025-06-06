from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
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

def init_db():
    """Initialize the database and create tables"""
    engine = create_engine('sqlite:///football_manager.db')
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Create a new database session"""
    engine = create_engine('sqlite:///football_manager.db')
    Session = sessionmaker(bind=engine)
    return Session()

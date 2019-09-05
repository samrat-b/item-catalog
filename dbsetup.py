from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import os
import sys

Base = declarative_base()


class Level(Base):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    details = Column(String(250))
    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship(Level)

# engine = create_engine('sqlite:///germancourse.db') 
engine = create_engine('sqlite:///germancourse.db', connect_args={'check_same_thread': False})  

Base.metadata.create_all(engine)    
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

    @property
    def serialize_levels(self):
        return{
            'id': self.id,
            'name': self.name
        }


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    details = Column(String(250))
    level_id = Column(Integer, ForeignKey('level.id'))
    level = relationship(Level)

    @property
    def serialize_courses(self):
        return{
            'id': self.id,
            'name': self.name,
            'details': self.details
        }


# engine = create_engine('sqlite:///germancourse.db')
# engine = create_engine('sqlite:///germancourse.db', connect_args={'check_same_thread': False})
engine = create_engine('sqlite:///germancourse.db' +
                       '?check_same_thread=False')


Base.metadata.create_all(engine)

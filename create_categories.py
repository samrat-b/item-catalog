from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbsetup import Level, Base
engine = create_engine('sqlite:///germancourse.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

level1 = Level(name="German for Beginners")

session.add(level1)
session.commit()

level2 = Level(name="Learn German Further")

session.add(level2)
session.commit()

level3 = Level(name="Master German Language")

session.add(level3)
session.commit()

print("Categories got created !")
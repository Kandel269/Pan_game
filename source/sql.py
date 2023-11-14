import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Boolean
from sqlalchemy.orm import sessionmaker

Base = sqlalchemy.orm.declarative_base()

class GameSettings(Base):
    __tablename__ = "settings"

    ssn = Column("ssn", Integer, primary_key=True, autoincrement=True)
    level = Column("level", Integer)
    sounds = Column("sounds", Boolean)

    def __init__(self, level,sounds):
        self.level = level
        self.sounds = sounds

engine = create_engine("sqlite:///settings.db", echo=True)
Base.metadata.create_all(bind = engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_data() -> (int, bool):
    my_settings = session.query(GameSettings).first()
    return my_settings.level, my_settings.sounds

def edit_data(level, sounds) -> None:
    my_settings = session.query(GameSettings).first()
    my_settings.level = level
    my_settings.sounds = sounds
    session.commit()
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://cacus_algo:1995@localhost:5432/cacus', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    time = Column(DateTime)

    def __repr__(self):
        return "Time recorded: " + datetime.strftime(self.time, "%H:%M - %a %d %b - %Y") + " Price: " + str(self.price)

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    closed = Column(Boolean, default=False)
    enter_price = Column(Float)
    exit_price = Column(Float, nullable=True)
    profit_loss = Column(Float, nullable=True)

Base.metadata.create_all(engine, checkfirst=True)
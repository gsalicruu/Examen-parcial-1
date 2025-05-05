from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///resultados.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Resultado(Base):
    __tablename__ = 'resultados'
    id = Column(Integer, primary_key=True)
    juego = Column(String(50))
    datos = Column(Text)

Base.metadata.create_all(engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "postgresql://user:password@postgres:5432/Echolink"

URL_DATABASE_LOCAL = "postgresql://user:password@localhost:5432/Echolink"


engine = create_engine(URL_DATABASE)

#engine = create_engine(URL_DATABASE_LOCAL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


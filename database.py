
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

sql_database_url= "mysql+pymysql://root@localhost:3306/revenue"
engine= create_engine(sql_database_url)
SessionLocal= sessionmaker(autocommit=False,autoflush=False, bind=engine)


Base= declarative_base()
print("connected")

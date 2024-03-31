from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()
URL_DATABASE = "mysql+pymysql://root:MANOsince%402003@localhost:3306/genai_v3"
print(URL_DATABASE)

engine = create_engine(URL_DATABASE)

session_local = sessionmaker(autocommit=False,autoflush=False, bind=engine)

base = declarative_base()
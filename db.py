import os
from sqlalchemy import MetaData, create_engine
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_NAME")

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@localhost:3306/{DATABASE}")

meta = MetaData()

connection = engine.connect()
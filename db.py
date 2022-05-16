from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root@localhost:3306/test")

connection = engine.connect()

# Fazer projeto
from sqlalchemy import Table, Column, Integer, String, Float, Date, MetaData, create_engine
from sqlalchemy.sql import text

# Crear el objeto MetaData
meta = MetaData()

# Crear la tabla "fastAPI"
users = Table("fastAPI", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(100)),
    Column("name", String(100)),
    Column("password", String(100)),
    Column("weight", Float),
    Column("date", Date)
)

# Crear el motor (engine) y conectar a la base de datos
engine = create_engine("mysql+pymysql://itxchewy:7300villa@db4free.net/base_aaron")

# Crear la tabla en la base de datos
meta.create_all(engine)

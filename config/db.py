from sqlalchemy import create_engine, MetaData

# Corrige el URI de la base de datos
engine = create_engine("mysql+pymysql://itxchewy:7300villa@db4free.net/base_aaron")

meta = MetaData()

# Establece la conexión con el nivel de aislamiento AUTOCOMMIT
conn = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
